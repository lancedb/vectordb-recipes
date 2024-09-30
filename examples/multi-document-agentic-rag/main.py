import os
import tqdm
import json
import time
from typing import List, Optional, Dict, Any
from tqdm import tqdm
import logging
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    Settings,
    Document,
)
from datetime import datetime, timedelta
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.tools import FunctionTool, ToolOutput
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.agent import AgentRunner

import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

OPENAI_API_KEY = "****"
if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# LLM setup
llm = OpenAI(model="gpt-4", api_key=OPENAI_API_KEY)

# Embedding model setup
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Update the Settings with the new embedding model
Settings.embed_model = embed_model
Settings.chunk_size = 512

# Vector store setup
problems_vector_store = LanceDBVectorStore(
    uri="./lancedb",
    table_name="problems_table",
    mode="overwrite",
)

parts_vector_store = LanceDBVectorStore(
    uri="./lancedb",
    table_name="parts_table",
    mode="overwrite",
)

diagnostics_vector_store = LanceDBVectorStore(
    uri="./lancedb",
    table_name="diagnostics_table",
    mode="overwrite",
)

cost_estimates_vector_store = LanceDBVectorStore(
    uri="./lancedb",
    table_name="cost_estimates_table",
    mode="overwrite",
)

maintenance_schedules_vector_store = LanceDBVectorStore(
    uri="./lancedb",
    table_name="maintenance_schedules_table",
    mode="overwrite",
)

cars_vector_store = LanceDBVectorStore(
    uri="./lancedb",
    table_name="car_maintenance_table",
    mode="overwrite",
)


def load_and_index_document_from_file(
    file_path: str, vector_store: LanceDBVectorStore
) -> VectorStoreIndex:
    """Load a document from a single file and index it."""
    with open(file_path, "r") as f:
        data = json.load(f)
        document = Document(text=json.dumps(data))

    parser = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
    nodes = parser.get_nodes_from_documents([document])
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex(nodes, storage_context=storage_context)


def create_retriever(index: VectorStoreIndex) -> VectorIndexRetriever:
    """Create a retriever from the index."""
    return index.as_retriever(similarity_top_k=5)


# Load and index documents directly from file paths
problems_index = load_and_index_document_from_file(
    "../multi-document-agentic-rag/json_files/problems.json", problems_vector_store
)
parts_index = load_and_index_document_from_file(
    "../multi-document-agentic-rag/json_files/parts.json", parts_vector_store
)
cars_index = load_and_index_document_from_file(
    "../multi-document-agentic-rag/json_files/cars_models.json", cars_vector_store
)
diagnostics_index = load_and_index_document_from_file(
    "../multi-document-agentic-rag/json_files/diagnostics.json",
    diagnostics_vector_store,
)
cost_estimates_index = load_and_index_document_from_file(
    "../multi-document-agentic-rag/json_files/cost_estimates.json",
    cost_estimates_vector_store,
)
maintenance_schedules_index = load_and_index_document_from_file(
    "../multi-document-agentic-rag/json_files/maintenance.json",
    maintenance_schedules_vector_store,
)

# Create retrievers
problems_retriever = create_retriever(problems_index)
parts_retriever = create_retriever(parts_index)
cars_retriever = create_retriever(cars_index)
diagnostics_retriever = create_retriever(diagnostics_index)
cost_estimates_retriever = create_retriever(cost_estimates_index)
maintenance_schedules_retriever = create_retriever(maintenance_schedules_index)


def retrieve_problems(query: str) -> str:
    """Searches the problem catalog to find relevant automotive problems for the query."""
    docs = problems_retriever.retrieve(query)
    information = str([doc.text[:200] for doc in docs])
    return information


def retrieve_parts(query: str) -> str:
    """Searches the parts catalog to find relevant parts for the query."""
    docs = parts_retriever.retrieve(query)
    information = str([doc.text[:200] for doc in docs])
    return information


def retrieve_car_details(make: str, model: str, year: int) -> str:
    """Retrieves the make, model, and year of the car."""
    docs = car_details_retriever.retrieve(make, model, year)
    information = str([doc.text[:200] for doc in docs])


def diagnose_car_problem(symptoms: str) -> str:
    """Uses the diagnostics database to find potential causes for given symptoms."""
    docs = diagnostics_retriever.retrieve(symptoms)
    information = str([doc.text[:200] for doc in docs])
    return information


def estimate_repair_cost(problem: str) -> str:
    """Provides a cost estimate for a given car problem or repair."""
    docs = cost_estimates_retriever.retrieve(problem)
    information = str([doc.text[:200] for doc in docs])
    return information


def get_maintenance_schedule(mileage: int) -> str:
    """Retrieves the recommended maintenance schedule based on mileage."""
    docs = maintenance_schedules_retriever.retrieve(str(mileage))
    information = str([doc.text[:200] for doc in docs])
    return information


def comprehensive_diagnosis(symptoms: str) -> str:
    """
    Provides a comprehensive diagnosis including possible causes, estimated costs, and required parts.

    Args:
        symptoms: A string describing the car's symptoms.

    Returns:
        A string with a comprehensive diagnosis report.
    """
    # Use existing tools
    possible_causes = diagnose_car_problem(symptoms)

    # Extract the most likely cause (this is a simplification)
    likely_cause = possible_causes[0] if possible_causes else "Unknown issue"

    estimated_cost = estimate_repair_cost(likely_cause)
    required_parts = retrieve_parts(likely_cause)

    report = f"Comprehensive Diagnosis Report:\n\n"
    report += f"Symptoms: {symptoms}\n\n"
    report += f"Possible Causes:\n{possible_causes}\n\n"
    report += f"Most Likely Cause: {likely_cause}\n\n"
    report += f"Estimated Cost:\n{estimated_cost}\n\n"
    report += f"Required Parts:\n{required_parts}\n\n"
    report += "Please note that this is an initial diagnosis. For accurate results, please consult with our professional mechanic."

    return report


def get_car_model_info(
    mileage: int, car_make: str, car_model: str, car_year: int
) -> dict:
    """Retrieve car model information from cars_models.json."""
    with open("cars_models/cars_models.json", "r") as file:
        car_models = json.load(file)

    for car in car_models:
        if (
            car["car_make"].lower() == car_make.lower()
            and car["car_model"].lower() == car_model.lower()
            and car["car_year"] == car_year
        ):
            return car
    return {}


def retrieve_car_details(make: str, model: str, year: int) -> str:
    """Retrieves the make, model, and year of the car and return the common issues if any."""
    car_details = get_car_model_info(
        0, make, model, year
    )  # Using 0 for mileage to get general details
    if car_details:
        return f"{year} {make} {model} - Common Issues: {', '.join(car_details['common_issues'])}"
    return f"{year} {make} {model} - No common issues found."


def plan_maintenance(mileage: int, car_make: str, car_model: str, car_year: int) -> str:
    """
    Creates a comprehensive maintenance plan based on the car's mileage and details.

    Args:
        mileage: The current mileage of the car.
        car_make: The make of the car.
        car_model: The model of the car.
        car_year: The year the car was manufactured.

    Returns:
        A string with a comprehensive maintenance plan.
    """
    car_details = retrieve_car_details(car_make, car_model, car_year)
    car_model_info = get_car_model_info(mileage, car_make, car_model, car_year)

    plan = f"Maintenance Plan for {car_year} {car_make} {car_model} at {mileage} miles:\n\n"
    plan += f"Car Details: {car_details}\n\n"

    if car_model_info:
        plan += f"Common Issues:\n"
        for issue in car_model_info["common_issues"]:
            plan += f"- {issue}\n"

        plan += f"\nEstimated Time: {car_model_info['estimated_time']}\n\n"
    else:
        plan += (
            "No specific maintenance tasks found for this car model and mileage.\n\n"
        )

    plan += "Please consult with our certified mechanic for a more personalized maintenance plan."

    return plan


def create_calendar_invite(
    event_type: str, car_details: str, duration: int = 60
) -> str:
    """
    Simulates creating a calendar invite for a car maintenance or repair event.

    Args:
        event_type: The type of event (e.g., "Oil Change", "Brake Inspection").
        car_details: Details of the car (make, model, year).
        duration: Duration of the event in minutes (default is 60).

    Returns:
        A string describing the calendar invite.
    """
    # Simulate scheduling the event for next week
    event_date = datetime.now() + timedelta(days=7)
    event_time = event_date.replace(hour=10, minute=0, second=0, microsecond=0)

    invite = f"Calendar Invite Created:\n\n"
    invite += f"Event: {event_type} for {car_details}\n"
    invite += f"Date: {event_time.strftime('%Y-%m-%d')}\n"
    invite += f"Time: {event_time.strftime('%I:%M %p')}\n"
    invite += f"Duration: {duration} minutes\n"
    invite += f"Location: Your Trusted Auto Shop, 123 Main St, Bengaluru, India\n\n"

    return invite


def coordinate_car_care(
    query: str, car_make: str, car_model: str, car_year: int, mileage: int
) -> str:
    """
    Coordinates overall car care by integrating diagnosis, maintenance planning, and scheduling.

    Args:
        query: The user's query or description of the issue.
        car_make: The make of the car.
        car_model: The model of the car.
        car_year: The year the car was manufactured.
        mileage: The current mileage of the car.

    Returns:
        A string with a comprehensive car care plan.
    """
    car_details = retrieve_car_details(car_make, car_model, car_year)

    # Check if it's a problem or routine maintenance
    if "problem" in query.lower() or "issue" in query.lower():
        diagnosis = comprehensive_diagnosis(query)
        plan = f"Based on your query, here's a diagnosis:\n\n{diagnosis}\n\n"

        # Extract the most likely cause (this is a simplification)
        likely_cause = diagnosis.split("Most Likely Cause:")[1].split("\n")[0].strip()

        # Create a calendar invite for repair
        invite = create_calendar_invite(f"Repair: {likely_cause}", car_details)
        plan += f"I've prepared a calendar invite for the repair:\n\n{invite}\n\n"
    else:
        maintenance_plan = plan_maintenance(mileage, car_make, car_model, car_year)
        plan = f"Here's your maintenance plan:\n\n{maintenance_plan}\n\n"

        # Create a calendar invite for the next maintenance task
        next_task = maintenance_plan.split("Task:")[1].split("\n")[0].strip()
        invite = create_calendar_invite(f"Maintenance: {next_task}", car_details)
        plan += f"I've prepared a calendar invite for your next maintenance task:\n\n{invite}\n\n"

    plan += "Remember to consult with a professional mechanic for personalized advice and service."

    return plan


## Create function tools
retrieve_problems_tool = FunctionTool.from_defaults(fn=retrieve_problems)
retrieve_parts_tool = FunctionTool.from_defaults(fn=retrieve_parts)
diagnostic_tool = FunctionTool.from_defaults(fn=diagnose_car_problem)
cost_estimator_tool = FunctionTool.from_defaults(fn=estimate_repair_cost)
maintenance_schedule_tool = FunctionTool.from_defaults(fn=get_maintenance_schedule)
comprehensive_diagnostic_tool = FunctionTool.from_defaults(fn=comprehensive_diagnosis)
maintenance_planner_tool = FunctionTool.from_defaults(fn=plan_maintenance)
calendar_invite_tool = FunctionTool.from_defaults(fn=create_calendar_invite)
car_care_coordinator_tool = FunctionTool.from_defaults(fn=coordinate_car_care)
retrieve_car_details_tool = FunctionTool.from_defaults(fn=retrieve_car_details)

tools = [
    retrieve_problems_tool,
    retrieve_parts_tool,
    diagnostic_tool,
    cost_estimator_tool,
    maintenance_schedule_tool,
    comprehensive_diagnostic_tool,
    maintenance_planner_tool,
    calendar_invite_tool,
    car_care_coordinator_tool,
    retrieve_car_details_tool,
]


# Function to reset the agent's memory
def reset_agent_memory():
    global agent_worker, agent
    agent_worker = FunctionCallingAgentWorker.from_tools(tools, llm=llm, verbose=True)
    agent = AgentRunner(agent_worker)


# Initialize the agent
reset_agent_memory()

response = agent.chat(
    "My car has 60,000 miles on it. What maintenance should I be doing now, and how much will it cost?"
)

print(f"LLM Response : {response}")
