

import os
from typing import Annotated, TypedDict
import tempfile
import streamlit as st
from pydantic import BaseModel
from langgraph.graph import StateGraph
from lancedb.rerankers import LinearCombinationReranker
from langchain_core.messages import HumanMessage, AIMessageChunk
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langchain.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import LanceDB
from langchain_community.tools import TavilySearchResults
from langchain_community.tools.bing_search import BingSearchResults
from langchain_community.tools.polygon.financials import PolygonFinancials
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter



os.environ["ANTHROPIC_API_KEY"] = ""
os.environ["TAVILY_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""
os.environ["POLYGON_API_KEY"]=  ''

def load_documents(uploaded_files):
    documents = []
    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith(".pdf"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            loader = PyPDFLoader(temp_file_path)
            documents.extend(loader.load())
        elif uploaded_file.name.endswith(".docx"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            loader = Docx2txtLoader(temp_file_path)
            documents.extend(loader.load())
        else:
            st.warning(f"Unsupported file type: {uploaded_file.name}")
            continue
    return documents

def main():
    st.set_page_config(page_title="Stock Market MultitAgent Chatbot  ", page_icon="📈", layout="centered", initial_sidebar_state="expanded")

    st.title("📈 Stock Market MultitAgent Chatbot")

    with st.sidebar:
        st.header("Upload Documents")
        st.markdown(
            "Upload your **stock market-related files** (PDF or DOCX) here to build a knowledge base for queries."
        )
        uploaded_files = st.file_uploader(
            "Drag and drop or browse files", type=["pdf", "docx"], accept_multiple_files=True
        )

        if not uploaded_files:
            st.warning("Please upload PDF or DOCX files related to the stock market to proceed.")
            return  # Exit

        if uploaded_files:
            documents = load_documents(uploaded_files)
            st.success(f"Loaded documents.")

            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200, length_function=len
            )
            splits = text_splitter.split_documents(documents)

            # Generate embeddings
            embeddings_n = OpenAIEmbeddings()
            reranker = LinearCombinationReranker(weight=0.3)
            docsearch = LanceDB.from_documents(splits, embeddings_n, reranker=reranker)
            st.success("Embeddings and retriever are ready.")

            class RagToolSchema(BaseModel):
                question: str

            @tool(args_schema=RagToolSchema)
            def retriever_tool(question):
                """Answer stock market-related questions using RAG."""
                retriever_result = docsearch.similarity_search_with_relevance_scores(question)
                return retriever_result

            tavilytool = TavilySearchResults(
                max_results=5,
                search_depth="advanced",
                include_answer=True,
                include_raw_content=True,
            )

            api_wrapper = PolygonAPIWrapper()
            financials_tool = PolygonFinancials(api_wrapper=api_wrapper)

            tools = [retriever_tool, financials_tool, tavilytool,bing_tool]
            llm = ChatOpenAI(model_name="gpt-4o")
            llm_with_tools = llm.bind_tools(tools=tools)

            class State(TypedDict):
                messages: Annotated[list, add_messages]

            graph_builder = StateGraph(State)

            def chatbot(state: State):
                return {"messages": [llm_with_tools.invoke(state["messages"])]}

            graph_builder.add_node("chatbot", chatbot)
            tool_node = ToolNode(tools=tools)
            graph_builder.add_node("tools", tool_node)

            graph_builder.add_conditional_edges(
                "chatbot",
                tools_condition,
            )
            graph_builder.add_edge("tools", "chatbot")
            graph_builder.add_edge(START, "chatbot")
            graph = graph_builder.compile()

    st.header("Ask a Question")
    st.markdown(
        "Type your **stock market-related question** in the search box below. The chatbot will use the uploaded documents to generate answers."
    )
    query = st.text_input("Enter your question:", placeholder="E.g. What are the financial statements of AAPL ")

    if query:
        inputs = [HumanMessage(content=query)]
        result = ""
        first_chunk = True

        st.write("Response:")
        placeholder = st.empty()

        for msg, metadata in graph.stream({"messages": inputs}, stream_mode="messages"):
            if msg.content and not isinstance(msg, HumanMessage):
                if isinstance(msg, AIMessageChunk):
                    if first_chunk:
                        result = msg.content
                        first_chunk = False
                    else:
                        result += msg.content
                    placeholder.write(result)
                elif isinstance(msg, AIMessageChunk):
                    result += msg.content
                    placeholder.write(result)

if __name__ == "__main__":
    main()
