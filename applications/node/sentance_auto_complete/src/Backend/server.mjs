// server.js
import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import { getRetrieverResponse, runLangChainProcess} from "./langchainProcessor.mjs";
import { TextLoader } from 'langchain/document_loaders/fs/text';
import path from 'path';
import multer from "multer";
import AbortController from 'abort-controller'
const app = express();
const port = 5300;
const allowedOrigin = "http://localhost:3000"; // Replace with your client-side application URL
const upload = multer({ dest: 'uploads/' }); // Temporary upload folder
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
app.post("/upload-file", upload.single("file"), async (req, res) => {
  try {
    const file = req.file;
    const fileType = path.extname(file.originalname).slice(1).toLowerCase();
    if (['txt'].includes(fileType)) {//can include other types of files
      const filePath =  file.path;
      const rawDocs = await loadDocument(filePath, fileType);
      await runLangChainProcess(rawDocs);
      res.json({
        message: 'File processed successfully',
      });
    } else {
      res.status(400).json({
        error: 'Unsupported file type'
      });
    }
  } catch (error) {
    res.status(500).json({
      error: 'Error processing file'
    });
  }
});

app.post("/process-text", async (req, res) => {
  try {
    const text = req.body.text;
    const modelName = req.body.text.modelName || 'gpt-4o-mini';
    let result;
    if (text !== "<p><br></p>") {
      result = await getRetrieverResponse(text, modelName);
    } else {
      result = [];
    }
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
    await runLangChainProcess(); // Initialize the process here
    console.log('LangChain process initialized successfully.');
  } catch (error) {
    console.error('Error initializing LangChain process:', error);
    process.exit(1);
  }
}

// Call the startServer function
startServer();