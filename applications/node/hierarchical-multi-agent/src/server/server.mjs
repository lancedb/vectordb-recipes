import express from "express";
import cors from "cors";
import fs from "fs";
import {
  LanceDB
} from "@langchain/community/vectorstores/lancedb";
import {
  RecursiveCharacterTextSplitter
} from 'langchain/text_splitter';
import {
  PDFLoader
} from "@langchain/community/document_loaders/fs/pdf";
import {
  connect
} from "@lancedb/lancedb";
import {
  OpenAIEmbeddings,
  ChatOpenAI,
  OpenAI
} from "@langchain/openai";
import dotenv from "dotenv";
import {
  createSupervisor
} from "@langchain/langgraph-supervisor";
import {
  createReactAgent
} from "@langchain/langgraph/prebuilt";
import {
  tool
} from "@langchain/core/tools";
import {
  z
} from "zod";
import {
  LLMChain
} from "langchain/chains";
import {
  PromptTemplate
} from "@langchain/core/prompts";

dotenv.config();

const app = express();
const allowedOrigin = "http://localhost:5173"
app.use(cors());
app.use(express.json());
let retriever;
let retrived_result;
const DB_PATH = "./db/legal_assistant.db";
const IPC_PDF_PATH = "src/server/data/ipc.pdf";
const NARCOTICS_PDF_PATH = "src/server/data/narcotics.pdf";
const model = new ChatOpenAI({
  model: 'gpt-4o-mini'
});

const llm = new OpenAI({
  modelName: "gpt-4o-mini",
  temperature: 0.7,
  maxTokens: 1000,
  maxRetries: 5,
});
const globalTrigger = {
  _listener: null,
  on(listener) {
    this._listener = listener;
  },
  trigger(data) {
    if (this._listener) {
      this._listener(data);
    }
  },
};

async function processAndStorePDFs(pdfPaths) {
  try {
    console.log("Loading PDFs...");
    let allDocs = [];
    // Load each PDF and extract text
    for (const pdfPath of pdfPaths) {
      const loader = new PDFLoader(pdfPath);
      const rawDocs = await loader.load();
      allDocs.push(...rawDocs);
    }

    // Split text into chunks
    const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 500,
      chunkOverlap: 10,
    });
    const docs = await splitter.splitDocuments(allDocs);
    const cleanDocs = docs.map(doc => ({
      pageContent: String(doc.pageContent),
      metadata: "{}",
    }));
    console.log("Generating embeddings...");
    const vectorStore = await LanceDB.fromDocuments(cleanDocs, new OpenAIEmbeddings());
    retriever = vectorStore.asRetriever();
    console.log("Embeddings stored in VectorStore successfully!", );
    return vectorStore.asRetriever();
  } catch (error) {
    console.error("Error in processing PDFs:", error);
    throw error;
  }
}

// Function to retrieve data using the global retriever variable
export async function retrieveContext(inputText) {
  if (!retriever) {
    throw new Error('Retriever is not initialized. Please run the initialization first.');
  }
  try {
    // Use the global retriever to retrieve results
    const retrieverResult = await retriever.invoke(inputText);
    if (retrieverResult.length === 0) {
      return "No relevant data found for the query.";
    }
    // Concatenate the relevant retrieved documents
    const retrievedDocs = retrieverResult.map(doc => doc.pageContent).join('\n\n');
    const prompt = `
      The user has provided the following text: "${inputText}"
     based on the input text...filter out the most relevent piece of information from the retived Docs below
      "${retrievedDocs}" keep it about 50 words long..basically you must clean up the retrived docs and create a meaningful text relevent to the input text`;
    const llmCompletion = await model.invoke(
      prompt
    );
    return llmCompletion.content;
  } catch (error) {
    console.error('Error during retrieval:', error);
    throw error;
  }
}


const summaryTool = tool(
  async (args) => {
    globalTrigger.trigger("Interpreting the section and extracting key details about it...");
    const query = args.query;
    const response = await llm.call(query);
    return response;
  }, {
    name: "summary_tool",
    description: "get me a detailed summary of the case",
    schema: z.object({
      query: z.string()
    }),
  }
);

const releventCasesTool = tool(
  async (args) => {
    setTimeout(() => {
      globalTrigger.trigger("Searching for relevant case laws and precedents.....");
    }, 100);
    const query = args.query;
    const response = await llm.call(query);
    return response;
  }, {
    name: "relevent_cases_tool",
    description: "return a list of relevent or similar or example cases of the case",
    schema: z.object({
      query: z.string()
    }),
  }
);

const IPCcasesAgent = createReactAgent({
  llm: model,
  tools: [summaryTool, releventCasesTool],
  name: "ipc_agent",
  prompt: "You are a IPC cases expert. Always use one tool at a time only one after the other. you are tasked to return the reponse summary in the format like the section of the law then explaination of the law, then punishment as heading and what is the punishment then related sections, use summaryTool for this and at last similar cases heading and 2-5 examples of past cases related with the case. use releventCasesTool for this. Always return the response in valid HTML tags.Use headings, paragraphs, lists, and tables where appropriate to make the response visually appealing"
});

const NarcoticsCasesAgent = createReactAgent({
  llm: model,
  tools: [summaryTool, releventCasesTool],
  name: "narcotics_agent",
  prompt: "You are a Narcotics cases expert. Always use one tool at a time only one after the other. you are tasked to return the reponse on the format like first mention the section of the law then explaination of the law, then punishment as heading and what is the punishment then related sections and at last similar cases heading and 2-5 examples of past cases related with the case. Always return the response in valid HTML tags.Use headings, paragraphs, lists, and tables where appropriate to make the response visually appealing"
});



async function callSupervisorAgent(query, sendUpdate) {
  // Create supervisor workflow
  sendUpdate("Supervisor has started analyzing your query and breaking it down into tasks......");
  const workflow = createSupervisor({
    agents: [IPCcasesAgent, NarcoticsCasesAgent],
    llm: model,
    prompt: "You are a team supervisor managing a IPC laws expert and a Narcotics expert. " +
      "For IPC crime events, use ipc_agent. " +
      "For narcotics drugs events, use narcotics_agent.",
    outputModel: "full_history",
    addHandoffBackMessages: true
  });
  // Compile and run
  const app = workflow.compile();
  const result = await app.invoke({
    messages: [{
      role: "user",
      content: query
    }]
  });
  const ipcAgentMessages = result.messages.filter(
    (msg) =>
    (msg.name === "ipc_agent" || msg.name === 'narcotics_agent') &&
    msg.content !== "Transferring back to supervisor"
  );
  return ipcAgentMessages;
}

// 📌 API Route to handle user queries
app.post("/query", async (req, res) => {
  try {
    const {
      query
    } = req.body;
    if (!query) return res.status(400).json({
      error: "Query is required."
    });
    res.write("Retrieving relevant legal context for you query...\n\n");
    retrived_result = await retrieveContext(query);

    globalTrigger.on((data) => {
      res.write(data);
    });

    let finalRes = await callSupervisorAgent(retrived_result, (status) => {
      res.write(status);
    });
    if (finalRes.length){
    res.write(`Final result: ${finalRes[0].content}\n\n`);
    } else {
      res.write(`Something went wrong: ${finalRes}\n\n`);
    }
    res.write("Retrival completed!\n\n");
    res.end();
  } catch (error) {
    console.error("Error processing query:", error);
    res.write(error);
    res.end();
  }
});

//Start server
async function server() {
  await processAndStorePDFs([IPC_PDF_PATH,NARCOTICS_PDF_PATH]);
  app.listen(5400, () => console.log("Server running on port 5400"));
};


server();