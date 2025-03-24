import express from "express";
import fs from "fs";
import csvParser from "csv-parser";
import {
  connect
} from "@lancedb/lancedb";
import {
  LanceDB
} from "@langchain/community/vectorstores/lancedb";
import {
  OpenAIEmbeddings
} from "@langchain/openai";
import {
  RecursiveCharacterTextSplitter
} from "langchain/text_splitter";
import cors from "cors";
import {
  OpenAI
} from '@langchain/openai';
import bodyParser from "body-parser";
import dotenv from 'dotenv';
import lancedb
from '@lancedb/lancedb';

dotenv.config();
const port = 5400;
const app = express();
let vectorStore;
const allowedOrigin = "http://localhost:5173"; // Replace with your client-side application URL
app.use(express.json());
app.use(
  cors({
    origin: allowedOrigin,
    methods: "GET, POST", // Specify allowed methods
    credentials: true, // Allow cookies for authenticated requests (if applicable)
    allowedHeaders: ["Content-Type"],
  })
);
app.use(bodyParser.json());
let retriever;
const embeddings = new OpenAIEmbeddings({
  apiKey: process.env.OPENAI_API_KEY
});
const llm = new OpenAI({
  temperature: 0.7, // Adjust based on how creative/responsive you want the LLM to be
  modelName: 'gpt-4o-mini', // Choose the model you're using, e.g., gpt - 4 or gpt - 3.5
  apiKey: process.env.OPENAI_API_KEY, // Replace with your API key or use dotenv to load it
});

async function getOrCreateLanceDBTable() {
  const db = await lancedb.connect(process.env.LANCEDB_URI);
  const tableNames = await db.tableNames();
  try {
    // Check if the table exists
    if (tableNames.includes(process.env.LANCEDB_TABLE_NAME || 'table'));
    console.log("Table already exists. Using existing table.");
  } catch (error) {
    // If the table doesn't exist, create a new one
    console.log("Table does not exist. Creating a new table.");
    const LANCEDB_URI = process.env.LANCEDB_URI || "database";
    const LANCEDB_TABLE_NAME = process.env.LANCEDB_TABLE_NAME || "table";
    const db = await connect(LANCEDB_URI);
  }
}

async function storeFeedback(feedbackData) {
  try {
    const table = await getOrCreateLanceDBTable();
    const documents = feedbackData.map((feedback) => ({
      pageContent: feedback.feedback,
      metadata: feedback
    }));
    const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 500,
      chunkOverlap: 5,
    });
    const chunks = await splitter.splitDocuments(documents);
    if (!vectorStore) {
      vectorStore = await LanceDB.fromDocuments(chunks, embeddings, {
        table
      });
    } else {
      await vectorStore.addDocuments(chunks);
    }
    return {
      success: true,
      message: "Feedback stored!"
    };
  } catch (error) {
    console.error("Error storing feedback:", error);
    return {
      success: false,
      message: "Error storing feedback"
    };
  }
}

async function getFeedbackScores(userId) {
  try {
    console.log("getting feedback score for:",userId);
    retriever = vectorStore.asRetriever();
    const results = await retriever.invoke(`get only with userId as: "${userId}"`);
    const output = results.map((result) => result.metadata);
    const outputNew = output.filter((result) => result.userId === userId);
    if (!results.length) {
      return {
        success: false,
        message: "No feedback found for user."
      };
    }
    return {
      success: true,
      user_id: userId,
      feedback: outputNew,
    };
  } catch (error) {
    console.error("Error analyzing feedback:", error);
    return {
      success: false,
      message: "Error getting feedback scores"
    };
  }
}

/** Function to retrieve and analyze feedback for a user */
async function analyzeFeedback(userId) {
  try {
    // Fetch all feedback embeddings for the user
    retriever = vectorStore.asRetriever();
    const results = await retriever.invoke(`get only with user id as: "${userId}"`);
    const output = results.map((result) => result.metadata);
    const outputNew = output.filter((result) => result.userId === userId);
    if (!results.length) {
      return {
        success: false,
        message: "No feedback found for user."
      };
    }
    // Combine all feedback for analysis
    const feedbackTexts = outputNew.map((r) => r.feedback).join("\n");
    // Simulated Ambient Agent Analysis
    const prompt = `From the input analyse the setiment of the comment and consider that also in you analysis and then also Analyze the following feedbacks and Proactively highlights key insights or areas for improvement state Aggregated feedback like summary in  text only and, sentiment analysis, Strengths and Weaknesses Analysis,and actionable insights.: "${feedbackTexts}"`;
    const llmCompletion = await llm.invoke(prompt, {
      prompt: prompt,
      maxTokens: 50,
      n: 4,
    });
    return {
      success: true,
      user_id: userId,
      feedback_analysis: llmCompletion,
    };
  } catch (error) {
    console.error("Error analyzing feedback:", error);
    return {
      success: false,
      message: "Error analyzing feedback"
    };
  }
}

app.post("/api/store-feedback", async (req, res) => {
  const {
    userId,
    feedback
  } = req.body;
  if (!userId || !feedback) {
    return res.status(400).json({
      success: false,
      message: "Missing data"
    });
  }
  const feedback_data = [{
    userId: userId,
    feedback: feedback
  }]
  const response = await storeFeedback(feedback_data);
  res.json(response);
});

/** API Route to Retrieve Feedback Analysis */
app.get("/api/analyze-feedback/:userId", async (req, res) => {
  const {
    userId
  } = req.params;
  const response = await analyzeFeedback(userId);
  res.json(response);
});

/** API Route to Retrieve Feedback Analysis */
app.get("/api/get-feedback/:userId", async (req, res) => {
  const {
    userId
  } = req.params;
  const response = await getFeedbackScores(userId);
  res.json(response);
});

// Initialize DB and start server
async function startServer() {
  try {
    console.log('LangChain process initialized successfully.');
  } catch (error) {
    console.error('Error initializing LangChain process:', error);
    process.exit(1);
  }
};
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

startServer();