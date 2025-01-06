import fs from 'fs';
import csvParser from 'csv-parser';
import {
  RecursiveCharacterTextSplitter
} from 'langchain/text_splitter';
import {
  OpenAIEmbeddings
} from '@langchain/openai';
import {
  LanceDB
} from '@langchain/community/vectorstores/lancedb';

let retriever;

// Function to read CSV and return structured data
async function readCSV(filePath) {
  return new Promise((resolve, reject) => {
    const rows = [];
    fs.createReadStream(filePath)
      .pipe(csvParser())
      .on('data', (data) => rows.push(data))
      .on('end', () => resolve(rows))
      .on('error', (error) => reject(error));
  });
}

// Function to process and store CSV data in LanceDB
export async function processCSVToVectorDB(filePath) {
  try {
    // Read CSV data
    const csvData = await readCSV(filePath);
    console.log('CSV Data Loaded:', csvData.length, 'rows');

    // Prepare data for vectorization
    const documents = csvData.map((row) => ({
      pageContent: Object.values(row).join(' '), // Combine row fields into a single text
      metadata: row, // Preserve the row metadata for retrieval
    }));

    // Split data into smaller chunks
    const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 25000,
      chunkOverlap: 1,
    });
    const docs = await splitter.splitDocuments(documents);

    // Store in LanceDB with OpenAI embeddings
    const vectorStore = await LanceDB.fromDocuments(docs.splice(0, 1000), new OpenAIEmbeddings());
    retriever = vectorStore.asRetriever(10);
    console.log('Data stored in LanceDB successfully.');
  } catch (error) {
    console.error('Error processing CSV to vector DB:', error);
    throw error;
  }
}

// Function to retrieve top 10 results based on a query
export async function getTopResults(query) {
  if (!retriever) {
    throw new Error('Retriever is not initialized. Please process the data first.');
  }

  try {
    const results = await retriever.invoke(query, {
      top_k: 10
    });
    const output = results.map((result) => result.metadata); // Extract row metadata
    return output;
  } catch (error) {
    console.error('Error retrieving results:', error);
    throw error;
  }
}

// Example Usage
export async function initializationOfDB() {
  const csvFilePath = 'src/Backend/dataSourceFiles/news.csv'; // Path to your CSV file
  try {
    await processCSVToVectorDB(csvFilePath); // Process CSV and store in LanceDB
  } catch (error) {
    console.error('Error:', error);
  }
};