# **Multi-Source RAG Agent for Export/Import Guidance**

This project implements a **multi-source RAG (Retrieval Augmented Generation) agent** to handle export and import queries. It uses **LanceDB** for document retrieval and **Tavily** for real-time external searches, helping users with export/import policies, product details, and related news.

## **Features**
- **3 Data Sources**:  
  - **Export/Import Guides**  
  - **Export Policies**  
  - **Import Policies**
  
- **Real-Time News**: Fetch the latest updates using **Tavily**.
- **Streaming Memory Support**: Track ongoing conversations.

## **Setup Instructions**
1. **Install dependencies**:

```bash
pip install langchain langchain_community langchain_openai lancedb langchain_text_splitters tavily
```

2. **Configure Directories**:  
   Define paths for your PDF directories containing documents related to export/import guides, export policies, and import policies.

3. **Document Manager**:  
   Loads and processes documents using **LanceDB** for retrieval and **OpenAIEmbeddings** for querying.

4. **Tools**:  
   - `guide_on_how_to_export`: Fetch export/import guides.
   - `export_policy`: Fetch export policies and related documents.
   - `import_policy`: Fetch import policies and HS codes.
   - `news_export`: Fetch real-time export/import news.

5. **Usage**:  
   Define a `graph` with the agent and use `print_stream` to display results. Example:

```python
inputs = {"messages": [("user", "How can I export organic chemicals?")]}
print_stream(graph.stream(inputs, stream_mode="values"))
```
