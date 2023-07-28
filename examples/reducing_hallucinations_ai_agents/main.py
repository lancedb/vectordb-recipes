import openai
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
from pydantic import BaseModel, Field
import argparse
import lancedb
import pytest

def embed_func(c):
    rs = openai.Embedding.create(input=c, engine=EMBEDDINGS_MODEL)
    return [record["embedding"] for record in rs["data"]]

class InsertCritiquesInput(BaseModel):
    info: str = Field(description="should be demographics or interests or other information about the exercise request provided by the user")
    actions: str = Field(description="numbered list of langchain agent actions taken (searched for, gave this response, etc.)")
    critique: str = Field(description="negative constructive feedback on the actions you took, limitations, potential biases, and more")


@tool("insert_critiques", args_schema=InsertCritiquesInput)
def insert_critiques(info: str, actions: str, critique: str) -> str:
    "Insert actions and critiques for similar exercise requests in the future."""
    table_name = "exercise-routine"
    if table_name not in db.table_names():
        tbl = db.create_table(table_name, [{"vector": embed_func(info)[0], "actions": actions, "critique": critique}])
    else:
        tbl = db.open_table(table_name)
        tbl.add([{"vector": embed_func(info)[0], "actions": actions, "critique": critique}])
    return "Inserted and done."

class RetrieveCritiquesInput(BaseModel):
    query: str = Field(description="should be demographics or interests or other information about the exercise request provided by the user")

@tool("retrieve_critiques", args_schema=RetrieveCritiquesInput)
def retrieve_critiques(query: str) -> str:
    "Retrieve actions and critiques for similar exercise requests."""
    table_name = "exercise-routine"
    if table_name in db.table_names():
        tbl = db.open_table(table_name)
        results = tbl.search(embed_func(query)[0]).limit(5).select(["actions", "critique"]).to_df()
        results_list = results.drop("vector", axis=1).values.tolist()
        return "Continue with the list with relevant actions and critiques which are in the format [[action, critique], ...]:\n" + str(results_list)
    else:
        return "No info, but continue."

def create_prompt(info: str) -> str:
    prompt_start = (
        "Please execute actions as a fitness trainer based on the information about the user and their interests below.\n\n"+
        "Info from the user:\n\n"
    )
    prompt_end = (
        "\n\n1. Retrieve using user info and review the past actions and critiques if there is any\n"+
        "2. Keep past actions and critiques in mind while researching for an exercise routine with steps which we respond to the user\n"+
        "3. Before returning the response, it is of upmost importance to insert the actions you took (numbered list: searched for, found this, etc.) and critiques (negative feedback: limitations, potential biases, and more) into the database for getting better exercise routines in the future. \n"
    )
    return prompt_start + info + prompt_end

def run_agent(info):
    agent = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    agent.run(input=create_prompt(info))

def args_parse():
    default_query = "university student, loves running"
    global EMBEDDINGS_MODEL

    parser = argparse.ArgumentParser(description='Reducing Hallucinations in AI Agents')
    parser.add_argument('--query', type=str, default=default_query, help='query to search')
    parser.add_argument('--llm', type=str, default="gpt-3.5-turbo-0613", help='OpenAI LLM')
    parser.add_argument('--embeddings', type=str, default="text-embedding-ada-002", help='OpenAI Embeddings Model')
    args = parser.parse_args()

    EMBEDDINGS_MODEL = args.embeddings

    return args

if __name__ == "__main__":
    args = args_parse()

    global db
    db = lancedb.connect("data/agent-lancedb")

    llm = ChatOpenAI(temperature=0, model=args.llm)
    tools = load_tools(["serpapi"], llm=llm)
    tools.extend([insert_critiques, retrieve_critiques])

    run_agent(args.query)


# TESTING ===========================================================

@pytest.fixture
def mock_embed_func(monkeypatch):
    def mock_api_call(*args, **kwargs):
        return {"data": [{"embedding": [0.1, 0.2, 0.3]}, {"embedding": [0.4, 0.5, 0.6]}]}
    monkeypatch.setattr(openai.Embedding, 'create', mock_api_call)

def test_main(mock_embed_func):
    args = argparse.Namespace(query="test", llm="test", embeddings="test")

    global db
    db = lancedb.connect("data/agent-lancedb")

    print(insert_critiques)
    print(retrieve_critiques)
