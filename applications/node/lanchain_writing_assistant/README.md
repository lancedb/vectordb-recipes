**AI Writing Assistant with LangChain.js and LanceDB**
======================================================

This project demonstrates an **AI-powered writing assistant** built using **LangChain.js** and **LanceDB**. The assistant utilizes **OpenAI's API** for language generation and LanceDB for efficient vector storage and retrieval, making it both scalable and customizable.

* * *

**Features**
------------

*   🔍 **Customizable Data**: Replace the default dataset with your own text files to tailor the assistant for domain-specific applications.
*   ⚡ **Efficient Retrieval**: Uses LanceDB to ensure low-latency and high-accuracy content retrieval.
*   🌐 **Scalable Architecture**: Built with modular components, making it easy to extend functionality or integrate with other tools.

* * *

**Demo**
--------

![LangChain.js + LanceDB Demo](https://github.com/lancedb/assets/blob/main/recipes/demo_vid_langchain_integration-ezgif.com-video-to-gif-converter.gif)

* * *

**Getting Started**
-------------------

### **1\. Prerequisites**

Ensure the following are installed:

*   Node.js (v20 or above)
*   NPM or Yarn
*   A valid [OpenAI API Key](https://platform.openai.com/signup)

* * *

### **2\. Installation**

Clone the repository and install the required dependencies:

`git clone`

`cd`

`npm install` 

* * *

### **3\. Configuration**

Set your OpenAI API key in your environment:

`export OPENAI_API_KEY=your_openai_key` 

Alternatively, create a `.env` file in the project root:


`OPENAI_API_KEY=your_openai_key` 

* * *

### **4\. Customizing the Dataset**

To use your own data:

1.  Navigate to the directory:
    
    
    `src/Backend/dataSourceFiles` 
    
2.  Replace the default `.txt` file with your own text file.
3.  Restart the server to apply changes.

* * *

### **5\. Running the Application**

Start the development server:

`npm run dev` 

Access the app in your browser at:

`http://localhost:3000` 

* * *

**Technical Details**
---------------------

### **How It Works**

1.  **Data Embedding**
    
    *   Text data from the `.txt` file is processed and converted into embeddings using OpenAI's embedding models.
2.  **Vector Storage and Retrieval**
    
    *   LanceDB stores and indexes the embeddings for fast similarity-based searches.
    *   When a user inputs a query, the system retrieves relevant text segments based on vector similarity.
3.  **Response Generation**
    
    *   LangChain.js orchestrates the interaction with OpenAI's API, using the retrieved context to generate meaningful responses.

* * *

**Commands**
------------

*   **Start the App**:
    
    `npm run dev` 

*   **Start the server only**:

    `npm run server`
    
*   **Replace Data**:  
    Place your `.txt` file in the `src/Backend/dataSourceFiles` directory and restart the server.
    

* * *

**Future Enhancements**
-----------------------

*   Support for additional file formats (e.g., `.csv`, `.json`).
*   Deployment to cloud platforms (e.g., Vercel, AWS).
*   A user-friendly interface for uploading and managing datasets.

* * *

Feel free to fork, contribute, and customize the project to suit your needs! 🎉
