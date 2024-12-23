**AI-Powered Article Recommendation System**
============================================

An advanced **AI-driven article recommendation engine** designed to process and retrieve **relevant articles** from a vast dataset of over **2 million articles**. This tool provides real-time, **context-aware article suggestions** by leveraging advanced **vector search** and **natural language processing (NLP)** technologies.

**Demo**
--------

![Real-Time Autocomplete Demo](./public/assests/article_recommendation_engine.gif)


* * * * *

**Features**
------------

-   🔍 **Keyword-Based Search**: Input any keyword or phrase, and get **top 10 relevant articles** instantly.
-   🌐 **Massive Dataset Support**: Efficiently processes and retrieves results from a **dataset of over 2 million articles**.
-   📈 **High Precision Recommendations**: Articles are ranked based on semantic similarity and relevance using state-of-the-art embeddings.
-   🧠 **AI-Powered Relevance**: Built with **LangChain.js** and **LanceDB** for robust NLP and vector search capabilities.

* * * * *

**How It Works**
----------------

1.  **Data Preprocessing**: Articles are divided into smaller, context-preserving chunks using **RecursiveCharacterTextSplitter**.\
    Example configuration:

    `const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 25000, // Adjust chunk size for optimal performance
      chunkOverlap: 1,  // Ensure overlap for context continuity
    });`

2.  **Vector Embedding**: The preprocessed data is embedded using **OpenAIEmbeddings**.
3.  **Efficient Storage**: Embedded vectors are stored in **LanceDB**, optimized for high-speed similarity search.
4.  **Query and Retrieval**: User input is matched against the dataset to retrieve **top 10 semantically similar articles**.

* * * * *

**Technical Highlights**
------------------------

-   **Advanced Vector Search**: Uses LanceDB to enable fast and scalable similarity searches across millions of articles.
-   **Real-Time Results**: The system retrieves and ranks articles within milliseconds.
-   **Customizable Dataset**: Easily replace the default dataset or upload custom datasets in `.csv` or `.txt` formats.

* * * * *

**Use Cases**
-------------

-   **Research and Academic Work**: Find articles that are most relevant to your research topic.
-   **Content Curation**: Discover the best content for blogs, newsletters, or social media.
-   **Media Monitoring**: Track trends and news articles efficiently.
-   **Educational Insights**: Access curated learning material on any subject.

* * * * *

**Getting Started**
-------------------

### **1\. Prerequisites**

-   **Node.js** version **20+**
-   A valid [OpenAI API Key](https://platform.openai.com/signup)

### **2\. Installation**

Clone the repository and install dependencies:


`git clone <repository-url>
cd <repository-folder>
npm install`

### **3\. Configure API Key**

Add your OpenAI API key in `.env`:

`OPENAI_API_KEY=your_openai_key`

* * * * *


### **4\. Add your data source**

Add your data source under the src>Backend>dataSourceFiles as news.csv
If you name it otherwise, you might have to change the data source link in langChainProcessor.mjs file

* * * * *

### **5\. Running the System**

use node >V20

`npm install`

#### Run Backend Server:

`npm run server`

#### Run Full Application:


`npm run dev`

Access the app at:

`http://localhost:5173`

* * * * *

**Customizing the Dataset**
---------------------------

You can upload or replace the dataset for customized recommendations:

1.  Navigate to `src/Backend/dataSourceFiles`.
2.  Replace the existing `.csv` or `.txt` file with your dataset.
3.  Restart the backend server to process the new dataset.

For example, to use the **All the News 2 Dataset**:\
[A dataset of 180mb size..used for creating this app](https://components.one/datasets/above-the-fold)\
[All the News 2 Dataset](https://components.one/datasets/all-the-news-2-news-articles-dataset)

* * * * *

**API Overview**
----------------

**Endpoint**: `/api/articles`\
**Method**: `POST`\
**Request Body**:

`{
  "text": "Your keyword here"
}`

**Response**:

`{
  "result": [
    {
      "metadata": {
        "title": "Sample Title",
        "author": "Author Name",
        "content": "Snippet of the article..."
      }
    }
  ]
}`

* * * * *

**Future Enhancements**
-----------------------

-   **Support for Multi-Modal Datasets**: Images, PDFs, and multimedia support.
-   **Interactive Filters**: Filter results by date, author, or publication.
-   **Deployable Cloud Versions**: Ready-to-deploy solutions for AWS, Vercel, and Netlify.
