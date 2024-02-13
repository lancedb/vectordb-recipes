import os
import dotenv
import gradio as gr
import lancedb
import logging
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import LanceDB
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import argostranslate.package
import argostranslate.translate


# Configuration Management
dotenv.load_dotenv(".env")
DB_PATH = "/tmp/lancedb"

COHERE_MODEL_NAME = "multilingual-22-12"
LANGUAGE_ISO_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Turkish": "tr",
    "French": "fr",
}

# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_documents_and_embeddings(input_file_path):
    """
    Initialize documents and their embeddings from a given file.

    Parameters:
    - input_file_path (str): The path to the input file. Supported formats are .txt and .pdf.

    Returns:
    - tuple: A tuple containing a list of texts split from the document and the embeddings object.
    """
    file_extension = os.path.splitext(input_file_path)[1]
    if file_extension == ".txt":
        logger.info("txt file processing")
        # Handle text file
        loader = TextLoader(input_file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)
    elif file_extension == ".pdf":
        logger.info("pdf file processing")
        # Handle PDF file
        loader = PyPDFLoader(input_file_path)
        texts = loader.load_and_split()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        texts = text_splitter.split_documents(texts)
    else:
        raise ValueError(
            "Unsupported file type. Supported files are .txt and .pdf only."
        )

    embeddings = CohereEmbeddings(model=COHERE_MODEL_NAME)
    return texts, embeddings


# Database Initialization
def initialize_database(texts, embeddings):
    """
    Initialize and populate a LanceDB database with documents and their embeddings.

    Parameters:
    - texts (list): A list of texts to be stored in the database.
    - embeddings (CohereEmbeddings): An embeddings object used to generate vector embeddings for the texts.

    Returns:
    - LanceDB: An instance of LanceDB with the documents and their embeddings stored.
    """
    db = lancedb.connect(DB_PATH)
    table = db.create_table(
        "multiling-rag",
        data=[
            {
                "vector": embeddings.embed_query("Hello World"),
                "text": "Hello World",
                "id": "1",
            }
        ],
        mode="overwrite",
    )
    return LanceDB.from_documents(texts, embeddings, connection=table)


# Translation Function
def translate_text(text, from_code, to_code):
    """
    Translate a given text from one language to another.

    Parameters:
    - text (str): The text to translate.
    - from_code (str): The ISO language code of the source language.
    - to_code (str): The ISO language code of the target language.

    Returns:
    - str: The translated text.
    """
    try:
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        package_to_install = next(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code,
                available_packages,
            )
        )
        argostranslate.package.install_from_path(package_to_install.download())
        return argostranslate.translate.translate(text, from_code, to_code)
    except Exception as e:
        logger.error(f"Error in translate_text: {str(e)}")
        return "Translation error"


prompt_template = """Text: {context}

Question: {question}

Answer the question based on the text provided. If the text doesn't contain the answer, reply that the answer is not available."""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


# Question Answering Function
def answer_question(question, input_language, output_language, db):
    """
    Answer a given question by retrieving relevant information from a database,
    translating the question and answer if necessary.
    Parameters:
    - question (str): The question to answer.
    - input_language (str): The language of the input question.
    - output_language (str): The desired language of the answer.
    - db (LanceDB): The LanceDB instance to use for information retrieval.

    Returns:
    - str: The answer to the question, in the desired output language
    """
    try:
        input_lang_code = LANGUAGE_ISO_CODES[input_language]
        output_lang_code = LANGUAGE_ISO_CODES[output_language]

        question_in_english = (
            translate_text(question, from_code=input_lang_code, to_code="en")
            if input_language != "English"
            else question
        )
        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        qa = RetrievalQA.from_chain_type(
            llm=Cohere(model="command", temperature=0),
            chain_type="stuff",
            retriever=db.as_retriever(),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True,
        )

        answer = qa({"query": question_in_english})
        result_in_english = answer["result"].replace("\n", "").replace("Answer:", "")

        return (
            translate_text(result_in_english, from_code="en", to_code=output_lang_code)
            if output_language != "English"
            else result_in_english
        )
    except Exception as e:
        logger.error(f"Error in answer_question: {str(e)}")
        return "An error occurred while processing your question. Please try again."


def setup_gradio_interface(db):
    """
    Setup a Gradio interface for interacting with the multilingual chatbot.

    Parameters:
    - db (LanceDB): The database instance to use for information retrieval.

    Returns:
    - gr.Interface: A Gradio interface object for the chatbot.
    """

    return gr.Interface(
        fn=lambda question, input_language, output_language: answer_question(
            question, input_language, output_language, db
        ),
        inputs=[
            gr.Textbox(lines=2, placeholder="Type your question here..."),
            gr.Dropdown(list(LANGUAGE_ISO_CODES.keys()), label="Input Language"),
            gr.Dropdown(list(LANGUAGE_ISO_CODES.keys()), label="Output Language"),
        ],
        outputs="text",
        title="Multilingual Chatbot",
        description="Ask any question in your chosen language and get an answer in the language of your choice.",
    )


# Main Function
def main():
    INPUT_FILE_PATH = "healthy-diet-fact-sheet-394.pdf"
    texts, embeddings = initialize_documents_and_embeddings(INPUT_FILE_PATH)
    db = initialize_database(texts, embeddings)
    iface = setup_gradio_interface(db)
    iface.launch(share=True, debug=True)


if __name__ == "__main__":
    main()
