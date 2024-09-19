// server.js
import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import {
  getRetrieverResponse,
  runLangChainProcess
} from "./langchainProcessor.mjs"; // Assume this file contains your main function logic

const app = express();
const port = 5300;
const allowedOrigin = "http://localhost:3000"; // Replace with your client-side application URL

app.use(
  cors({
    origin: allowedOrigin,
    methods: "GET, POST", // Specify allowed methods
    credentials: true, // Allow cookies for authenticated requests (if applicable)
    allowedHeaders: ["Content-Type"],
  })
);
app.use(bodyParser.json());

app.post("/process-text", async (req, res) => {
  try {
    const text = req.body.text;
    let result;
    if(text){
    result = await getRetrieverResponse(text);
    } else {
      result = "empty string";
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
    process.exit(1); // Exit the process with an error code
  }
}

// Call the startServer function
startServer();
