import os
import gradio as gr
import pymupdf4llm
from dotenv import load_dotenv
from tempfile import mkdtemp
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain_community.vectorstores import LanceDB
from lancedb.rerankers import LinearCombinationReranker
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredMarkdownLoader


# Load environment variables from .env file
load_dotenv()


# Temporary directory for file processing
temp_dir = mkdtemp()

# Define global variables for embeddings and docsearch
embeddings = None
docsearch = None


# Function to process the uploaded PDF file
def process_file(file):
    global embeddings, docsearch

    if file is None:
        return "No file uploaded. Please upload a PDF file."

    # Convert PDF to markdown
    md_text = pymupdf4llm.to_markdown(file.name, table_strategy="lines_strict")

    # Write markdown string to a file in the temporary directory
    md_file_path = os.path.join(temp_dir, "output_credit_card.md")
    with open(md_file_path, "w") as output:
        output.write(md_text)

    # Load the markdown file
    loader = UnstructuredMarkdownLoader(md_file_path)
    documents = loader.load()

    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    # Setup embeddings and vector store
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    reranker = LinearCombinationReranker(weight=0.3)
    docsearch = LanceDB.from_documents(chunks, embeddings, reranker=reranker)

    return "File processed successfully. You can now ask questions about the credit card statement."


# Function to process the query
def process_query(query):
    if docsearch is None:
        return "No document has been uploaded and processed yet. Please upload a PDF first."

    docs = docsearch.similarity_search(query)
    top_docs = docs[:2]  # Get only the top 2 documents
    response = chain(
        {"input_documents": top_docs, "human_input": query}, return_only_outputs=True
    )
    return response["output_text"]


# Define the prompt template
template = """
Your ability to extract and summarize this information accurately is essential for effective credit card statement analysis.
You are a financial expert AI chatbot having a conversation with a human.
Your task is to provide accurate and helpful answers based on the extracted parts of a credit card statement.
Pay close attention to the credit card statement's language, structure, and any cross-references to ensure comprehensive and precise extraction of information.
Do not use prior knowledge or information from outside the context to answer the questions.

If the human greets you then respond with a polite greeting.
If the question is not related to the credit card statement, respond with "Sorry, I don't know. Please ask questions related to the provided credit card statement."

Only use the information provided in the context to answer the questions.

Credit Card Statement Extract:
{context}

Conversation History:
{chat_history}

Human: {human_input}
Chatbot:
"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input", "context"], template=template
)

# Set up the memory and chain
memory = ConversationBufferMemory(memory_key="chat_history", input_key="human_input")
chain = load_qa_chain(
    OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY")),
    chain_type="stuff",
    memory=memory,
    prompt=prompt,
)

# Define the Gradio interfaces
upload_interface = gr.Interface(
    fn=process_file,
    inputs=gr.File(label="Upload your credit card statement PDF"),
    outputs="text",
    title="Credit Card Statement Upload",
    description="Upload your credit card statement PDF file to analyze.",
)

chat_interface = gr.Interface(
    fn=process_query,
    inputs=gr.Textbox(lines=2, placeholder="Enter your query here..."),
    outputs=gr.Textbox(),
    title="Credit Card Statement Analysis",
    description="Ask questions about the credit card statement.",
)

iface = gr.TabbedInterface(
    interface_list=[upload_interface, chat_interface],
    tab_names=["Upload PDF", "Chat with AI"],
)

# Launch the interface
iface.launch(share=True, debug=True)

# Clean up the temporary directory on exit
import atexit


def cleanup_temp_dir():
    shutil.rmtree(temp_dir)


atexit.register(cleanup_temp_dir)
