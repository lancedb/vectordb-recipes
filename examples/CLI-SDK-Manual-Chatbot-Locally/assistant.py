from rich.prompt import Prompt
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.lancedb import LanceDb
from phi.embedder.ollama import OllamaEmbedder

# loading document with their openhermes embedding in LanceDB
pdf_knowledge_base = PDFKnowledgeBase(
    path="data/manual.pdf",
    # Table name: ai.pdf_documents
    vector_db=LanceDb(
        embedder=OllamaEmbedder(),
        table_name="pdf_documents",
        uri="/tmp/lancedb",
    ),
    reader=PDFReader(chunk=True),
)

# define an assistance with llama3 llm and loaded knowledge base
assistant = Assistant(
    llm=Ollama(model="llama3"),
    description="You are an Expert in SDK or Hardware Manual assistant. Your task is to understand the user question, and provide an answer using the provided contexts. Every answer you generate should have citations in this pattern  'Answer [position].', for example: 'Earth is round [1][2].,' if it's relevant.Your answers are correct, high-quality, and written by an domain expert. If the provided context does not contain the answer, simply state, 'The provided context does not have the answer.'",
    knowledge_base=pdf_knowledge_base,
    add_references_to_prompt=True,
)
assistant.knowledge_base.load(recreate=False)

# start cli chatbot with knowledge base
assistant.print_response("Ask me about something from the knowledge base")
while True:
    message = Prompt.ask(f"[bold] :sunglasses: User [/bold]")
    if message in ("exit", "bye"):
        break
    assistant.print_response(message, markdown=True)
