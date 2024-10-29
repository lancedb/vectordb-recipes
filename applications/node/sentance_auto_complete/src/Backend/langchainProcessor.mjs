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
import {
  OpenAI
} from '@langchain/openai';

let retriever;
const llm = new OpenAI({
  temperature: 0.7, // Adjust based on how creative/responsive you want the LLM to be
  modelName: 'gpt-4o-mini', // Choose the model you're using, e.g., gpt - 4 or gpt - 3.5
  apiKey: 'process.env.OPENAI_API_KEY', // Replace with your API key or use dotenv to load it
});

export async function runLangChainProcess(rawDocsUploaded) {
  try {
    const loader = new TextLoader("src/Backend/dataSourceFiles/data.txt");
    let rawDocs = await loader.load();
    const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 500, // Flexible size, can be tweaked
      chunkOverlap: 50, // Adjust overlap if needed
      separators: ["\n\n", ".", "!", "?"], // Split on paragraphs or sentence boundaries for more meaningful chunks
    });
    if (rawDocsUploaded) {
      rawDocs = rawDocsUploaded;
    }

    const docs = await splitter.splitDocuments(rawDocs);

    const vectorStore = await LanceDB.fromDocuments(docs, new OpenAIEmbeddings());

    retriever = vectorStore.asRetriever();

  } catch (error) {
    console.error('Error in processing:', error);
    throw error;
  }
}

export async function getRetrieverResponse(inputText, modelName) {


  llm.modelName = modelName;
  if (!retriever) {
    throw new Error('Retriever is not initialized. Please run the initialization first.');
  }
  try {
    const retrieverResult = await retriever.invoke(inputText);
    if (retrieverResult.length === 0) {
      return "No relevant data found for the query.";
    }

    // Concatenate the relevant retrieved documents
    const retrievedDocs = retrieverResult.map(doc => doc.pageContent).join('\n\n');
    const prompt = `
      The user has provided the following text: "${inputText}"
      Provide 5 different completions, each within 50 tokens:
      Based on the following retrieved information, continue the user's sentence or suggest a meaningful continuation:
      "${retrievedDocs}"
      The continuation should flow naturally from the user's input, using the retrieved information as context and reference.
    `;

    // Use the LLM to complete the sentence or suggest a continuation based on user input and retrieved docs
    const llmCompletion = await llm.invoke(prompt, {
      prompt: prompt,
      maxTokens: 50,
      n: 4,
    });

    const suggestionsArray = llmCompletion
      .trim() // Remove any extra leading/trailing whitespace
      .split(/\d+\.\s+/) // Split based on the numbered pattern (e.g., '1. ', '2. ')
      .filter(Boolean) // Remove any empty elements from the array
      .map(item => item.replace(/(^"|"$)/g, '')); // Remove the surrounding quotation marks
    return suggestionsArray;
  } catch (error) {
    console.error('Error during retrieval or LLM completion:', error);
    throw error;
  }
}