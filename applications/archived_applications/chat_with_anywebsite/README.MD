# Chat with Any Website or URL

This project enables you to chat with any website or URL using advanced language models and vector embeddings. We have employed the state-of-the-art Mistral GGML model and BGE (BAAI) embedding, with LanceDB as the vector database to provide a powerful chatbot experience.

## Key Features

- **Mistral Model**: Our chatbot utilizes the [Mistral-7B-Instruct](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF) model. This model delivers performance equivalent to llama2-13B, making it a powerful conversational tool.

- **BGE Embedding**: We employ BGE (BAAI) embedding, which ranks first on the leaderboard, ensuring high-quality conversational responses.

- **LanceDB Vectorstore**: For efficient storage and retrieval, we use LanceDB as the vector database. This allows us to handle your chatbot interactions seamlessly.

## Getting Started


Follow these simple steps to run the application and chat with websites or URLs:

1. Clone this repository to your local machine.

2. Ensure you have Python 3 installed. this is tested on python 3.10

3. Install the required dependencies using the following command:

```
pip install -r requirements.txt
```

4. run the app
```
python3 app.py
```

5. Once the application is running, you can pass any website or URL, either a single URL or multiple URLs.

Example:


https://lancedb.com/ & https://blog.lancedb.com/context-aware-chatbot-using-llama-2-lancedb-as-vector-database-4d771d95c755


6. Start asking questions related to the provided website or URL.

7. You can use the "Clear" button to reset the chat and start a new conversation.

8. If you want to use new URLs, you'll need to run the application again.

 Feel free to experiment with different urls 
