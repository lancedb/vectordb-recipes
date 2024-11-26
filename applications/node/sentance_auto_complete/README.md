**Real-Time Autocomplete Suggestions with LangChain.js and LanceDB**

An AI-powered **real-time autocomplete suggestion tool** built with **LangChain.js** and **LanceDB**. Upload your data source, start typing your article, and receive **relevant sentence suggestions** in real-time. This tool dynamically predicts and completes your sentences, enhancing your writing flow. Additionally, you can seamlessly switch between different **GPT models** for varied outputs.

**Demo**
--------

![Real-Time Autocomplete Demo](https://github.com/lancedb/assets/blob/main/recipes/sentance_Auto_complete.gif)

**Features**
------------

*   ✍️ **Real-Time Suggestions**: Contextual, sentence-level suggestions to speed up your writing process.
*   📂 **Customizable Data Source**: Use your own datasets by uploading text files or replacing the default source.
*   🌟 **Switchable Models**: Easily toggle between GPT models for varied response styles.

**Getting Started**
-------------------

### **1\. Prerequisites**

Ensure you have:

*   **Node.js** version **20+** installed.
*   A valid [OpenAI API Key](https://platform.openai.com/signup).

### **2\. Installation**

#### Clone the Repository and Install Dependencies:


`git clone`

`cd `

`npm install` 

### **3\. Configuration**

Set your OpenAI API key in your environment:

`export OPENAI_API_KEY=your_openai_key` 

Alternatively, you can create a `.env` file in the project root:

`OPENAI_API_KEY=your_openai_key` 

### **4\. Running the Server Only**

To run just the backend server:

`npm run server` 


### **5\. Running the Full Application**

To run the full application locally:

`npm run dev` 

Access the app in your browser at:

`http://localhost:3000` 


**Customizing the Dataset**
---------------------------

### Upload or Replace the Data Source:

1.  Navigate to:
    
    plaintext
    
    Copy code
    
    `src/Backend/dataSourceFiles` 
    
2.  Replace the default `.txt` file with your custom text file **or** use the file upload functionality in the app.
3.  Restart the server to load the new dataset.

**Technical Overview**

### **How It Works**

1.  **Data Preprocessing and Embedding**
    
    *   Input data is tokenized and converted into embeddings using OpenAI's models.
2.  **Vector Search and Retrieval**
    
    *   LanceDB efficiently retrieves the most relevant text snippets based on similarity to the user's input.
3.  **Real-Time Sentence Suggestions**
    
    *   LangChain.js dynamically generates sentence-level completions tailored to the current context.
4.  **Model Switching**
    
    *   Easily toggle between GPT models in the application for diverse suggestions.

**Commands**

*   **Start the Backend Server**:

    `npm run server` 
    
*   **Run the Full Application**:
    
    `npm run dev` 
    
*   **Replace or Upload Data**:  
    Place your `.txt` file in the `src/Backend/dataSourceFiles` directory or use the file upload feature in the app.

**Future Enhancements**
-----------------------

*   Support for more file formats, such as `.csv` and `.json`.
*   Interactive UI for dataset uploads and management.
*   Deployable versions for cloud platforms like AWS, Vercel, or Netlify.

Feel free to fork, contribute, and customize this project for your unique requirements! 🚀
