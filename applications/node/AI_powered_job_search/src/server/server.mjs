// File: server.js
import express from "express";
import fs from "fs";
import csvParser from "csv-parser";
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

// Function to read and process CSV data
async function loadDataToVectorDB(filePath) {
  const rows = [];
  fs.createReadStream(filePath)
    .pipe(csvParser())
    .on("data", (data) => rows.push(data))
    .on("end", async () => {
      console.log("CSV data loaded:", rows.length, "rows");
      if (rows.length === 0) {
        console.error("No valid rows found for ingestion.");
        return;
      }
      console.log("Valid rows:", rows.length);
      const documents = rows.map((row) => ({
        pageContent: Object.values(row).join(" "),
        metadata: row,
      }));

      const splitter = new RecursiveCharacterTextSplitter({
        chunkSize: 1250,
        chunkOverlap: 5,
      });
      const chunks = await splitter.splitDocuments(documents);

      vectorStore = await LanceDB.fromDocuments(chunks.splice(0, 3000), new OpenAIEmbeddings());
      retriever = vectorStore.asRetriever(5);
    });
}

export async function getTopResults(query,new_filters) {
  if (!retriever) {
    throw new Error('Retriever is not initialized. Please process the data first.');
  }

  try {
    retriever = vectorStore.asRetriever(50);
    const results = await retriever.invoke(query);
    const output = results.map((result) => result.metadata);
    const filteredData = advancedFilter(output, new_filters);
     // Remove duplicates based on Job Id
     const seenJobIds = new Set();
     const uniqueResults = filteredData.filter((job) => {
       if (seenJobIds.has(job["Job Id"])) {
         return false;
       }
       seenJobIds.add(job["Job Id"]);
       return true;
     });

     return uniqueResults;
    return filteredData;
  } catch (error) {
    console.error("Error retrieving results:", error);
    throw error;
  }
}

// Endpoint for job search
app.post("/searchJobs", async (req, res) => {
  try {
    const text = req.body.body.text;
     const filters = {
       skills: req.body.body.skills || [],
       title: req.body.body.title || "",
       location: req.body.body.location || "",
       salaryRange: req.body.body.salary || [0, Infinity], // Default to 0-Infinity if not provided
     };
    let result;
    result = await getTopResults(text,filters);
    res.header("Access-Control-Allow-Origin", "*"); // Pass the text to your main function logic
    res.json({
      result, retriever
    });
  } catch (error) {
    console.log(error)
    res.status(500).send("Error processing the text");
  }
});

// Initialize DB and start server
async function startServer() {
  try {
    console.log('Starting LangChain server...');
    await loadDataToVectorDB("src/server/dataset/some_other_file.csv");
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

function advancedFilter(data, filters) {
  return data.filter((item) => {
    // Check if 'skills' filter exists and matches any skill in the item's skills
    const skillsMatch = !filters.skills.length || filters.skills.some((skill) => item.skills?.toLowerCase().includes(skill.toLowerCase())
    );

    // Check if 'location' filter exists and matches the item's location
    const locationMatch = !filters.location.length || filters.location.some((location) => item.location?.toLowerCase().includes(location.toLowerCase()))
    const countryMatch = !filters.location.length || filters.location.some((location) => item.Country?.toLowerCase().includes(location.toLowerCase())
    );

    // Check if 'salaryRange' filter exists and falls within the item's salary range
    let salaryRangeMatch = false;
    if (filters.salaryRange) {
      const [minSalary, maxSalary] = filters.salaryRange;
      const salaryRange = item["Salary Range"]?.match(/\$\d+K/g)?.map((salary) =>
        parseInt(salary.replace("$", "").replace("K", "")) * 1000
      );
      if (salaryRange) {
        salaryRangeMatch = minSalary <= salaryRange[0] && maxSalary >= salaryRange[1];
      }
    }
    // Return true if all filter matches
    return skillsMatch && (locationMatch || countryMatch) && salaryRangeMatch;
  });
}