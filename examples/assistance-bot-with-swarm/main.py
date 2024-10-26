import re

import lancedb
from swarm import Agent
from swarm.repl import run_demo_loop

db = lancedb.connect("/tmp/db")
table = db.open_table("help-center")


def query_lancedb(query, top_k=5):
    # Creates embedding vector from user query
    query_results = table.search(query).limit(top_k).to_pandas()

    return query_results


def query_docs(query):
    """Query the knowledge base for relevant articles."""
    print(f"Searching knowledge base with query: {query}")
    query_results = query_lancedb(query)
    output = []

    print(query_results)
    for index, article in query_results.iterrows():
        output.append((article["title"], article["text"], article["url"]))

    if output:
        title, content, _ = output[0]
        response = f"Title: {title}\nContent: {content}"
        truncated_content = re.sub(
            r"\s+", " ", content[:50] + "..." if len(content) > 50 else content
        )
        print("Most relevant article title:", truncated_content)
        return {"response": response}
    else:
        print("No results")
        return {"response": "No results found."}


def send_email(email_address, message):
    """Send an email to the user."""
    response = f"Email sent to: {email_address} with message: {message}"
    return {"response": response}


def submit_ticket(description):
    """Submit a ticket for the user."""
    return {"response": f"Ticket created for {description}"}


def transfer_to_help_center():
    """Transfer the user to the help center agent."""
    return help_center_agent


user_interface_agent = Agent(
    name="User Interface Agent",
    instructions="You are a user interface agent that handles all interactions with the user. Call this agent for general questions and when no other agent is correct for the user query.",
    functions=[transfer_to_help_center],
)

help_center_agent = Agent(
    name="Help Center Agent",
    instructions="You are an OpenAI help center agent who deals with questions about OpenAI products, such as GPT models, DALL-E, Whisper, etc.",
    functions=[query_docs, submit_ticket, send_email],
)

if __name__ == "__main__":
    run_demo_loop(user_interface_agent)
