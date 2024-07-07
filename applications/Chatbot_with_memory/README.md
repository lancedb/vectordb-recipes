# Credit Card Statement Analysis with AI Chatbot
This project uses AI to analyze credit card statements. By uploading a PDF file, the AI converts it to Markdown format, splits it into chunks, and allows you to ask questions about the statement. The project uses various libraries like Gradio, LangChain, and PyMuPDF4LLM to achieve this functionality.

# Features
- PDF to Markdown Conversion: Converts complex PDFs to Markdown for better understanding by LLMs.
- Chunk Splitting: Splits the document into manageable chunks for efficient processing.
- Question Answering: Uses AI to answer questions about the credit card statement based on the provided context


## Install  libraries
```
pip install langchain openai
pip install -qU langchain-text-splitters
pip install pypdf
pip install langchain_community
pip install pymupdf
pip install lancedb
pip install pymupdf4llm
pip install "unstructured[md]"
pip install -U langchain-openai langchain-community
pip install gradio
pip install tantivy
```


Make sure your PDF file (sample_credit_card.pdf) is accessible at the specified path.

Open a terminal or command prompt in the directory where the script is saved and run:

# Running the app
```
python main.py

```
