// langchainProcessor.js
import {
  RecursiveCharacterTextSplitter
} from 'langchain/text_splitter';
import {
  MemoryVectorStore
} from 'langchain/vectorstores/memory';
import {
  OpenAIEmbeddings
} from '@langchain/openai';
import {
  TextLoader
} from 'langchain/document_loaders/fs/text';
import {
  LanceDB
} from "@langchain/community/vectorstores/lancedb";


let retriever;

export async function runLangChainProcess() {
  try {
    console.log("called")
    const loader = new TextLoader("src/Backend/dataSourceFiles/data.txt");
    const rawDocs = await loader.load();
    const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 500,
      chunkOverlap: 10,
    });
    const docs = await splitter.splitDocuments(rawDocs);

    const vectorStore = await LanceDB.fromDocuments(docs, new OpenAIEmbeddings());
    console.log(vectorStore)
    retriever = vectorStore.asRetriever();
  } catch (error) {
    console.error('Error in processing:', error);
    throw error;
  }
}

// Function to retrieve data using the global retriever variable
export async function getRetrieverResponse(inputText) {
  if (!retriever) {
    throw new Error('Retriever is not initialized. Please run the initialization first.');
  }

  try {
    // Use the global retriever to retrieve results
    const retrieverResult = await retriever.invoke(inputText);
    return retrieverResult; // Return the retrieval result
  } catch (error) {
    console.error('Error during retrieval:', error);
    throw error;
  }
}