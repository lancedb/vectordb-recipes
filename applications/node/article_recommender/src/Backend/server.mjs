// server.js
import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import {
  initializationOfDB,
  getTopResults
} from "./langchainProcessor.mjs";
import {
  TextLoader
} from 'langchain/document_loaders/fs/text';
import path from 'path';
import multer from "multer";
import AbortController from 'abort-controller'
const app = express();
const port = 5300;
const allowedOrigin = "http://localhost:5173"; // Replace with your client-side application URL
let currentAbortController = null;

app.use(
  cors({
    origin: allowedOrigin,
    methods: "GET, POST", // Specify allowed methods
    credentials: true, // Allow cookies for authenticated requests (if applicable)
    allowedHeaders: ["Content-Type"],
  })
);
app.use(bodyParser.json());

async function loadDocument(filePath, fileType) {
  let loader;
  if (fileType === 'txt') {
    loader = new TextLoader(filePath);
  }
  return await loader.load();
}

// Handle file uploads
app.post("/api/articles", async (req, res) => {
  try {
    const text = req.body.text;
    let result;
    result = await getTopResults(text);
    res.header("Access-Control-Allow-Origin", "*"); // Pass the text to your main function logic
    res.json({
      result,
    });
  } catch (error) {
    res.status(500).send("Error processing the text");
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

async function startServer() {
  try {
    console.log('Starting LangChain process...');
    await initializationOfDB(); // Initialize the process here
    console.log('LangChain process initialized successfully.');
  } catch (error) {
    console.error('Error initializing LangChain process:', error);
    process.exit(1);
  }
}

// Call the startServer function
startServer();