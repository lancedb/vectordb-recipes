import express from "express";
import fs from "fs";
import {
  LanceDB
} from "@langchain/community/vectorstores/lancedb";
import {
  connect
} from "@lancedb/lancedb";
import path from "path";
import sharp from "sharp";
import axios from "axios";
import csvParser from "csv-parser";
import cors from "cors";
import bodyParser from "body-parser";

import dotenv from 'dotenv';
dotenv.config();

const size_of_input_data = 100;
const port = 5400;
const app = express();
const allowedOrigin = "http://localhost:5173"; // Replace with your client-side application URL
app.use(express.json({
  limit: "50mb"
}));
app.use(
  cors({
    origin: allowedOrigin,
    methods: "GET, POST",
    credentials: true,
    allowedHeaders: ["Content-Type"],
  })
);
app.use(bodyParser.json());

app.post("/retrive-results", async (req, res) => {
  try {
    const query = req.body.query;
    const table = req.body.table;
    let result;
    result = await retrieveContext(query, table)
    res.header("Access-Control-Allow-Origin", "*");
    res.json({
      result
    });
  } catch (error) {
    console.log(error)
    res.status(500).send("Error processing the text");
  }
});

async function retrieveContext(query, table) {
  console.log("retriving from db");
  const db = await connect(process.env.LANCEDB_URI || "database");
  const tableNames = await db.tableNames();
  const tbl = await db.openTable(table);
  if (!tbl) {
    console.log("table not found")
    await createEmbeddingsTable();
  }
  const result = await tbl.search(query).select(["img"]).limit(25).toArray();
  const retrived_results = result.map((r) => r.img);
  return retrived_results;
}

app.post("/get-embeddings", async (req, res) => {
  console.log("getting embeddings");
  try {
    const data = req.body.data;
    const type = req.body.type;
    let result;
    result = await getEmbeddings(data, type);
    res.header("Access-Control-Allow-Origin", "*");
    res.json({
      result
    });
  } catch (error) {
    console.log(error)
    res.status(500).send("Error getting embeddings");
  }
});

async function extractColumnFromCSV(path, columnIndex) {
  return new Promise((resolve, reject) => {
    let columnValues = [];

    fs.createReadStream(path)
      .pipe(csvParser())
      .on("data", (row) => {
        const values = Object.values(row);
        if (values.length > columnIndex) {
          columnValues.push(values[columnIndex]); // Extract value at 3rd column index..you canchange this as per your data
        }
      })
      .on("end", () => resolve(columnValues))
      .on("error", (err) => reject(err));
  });
}

async function processImgsAndText(imgs_dir, text_dir, db) {
  console.log("processing images and texts")
  const imgs = fs.readdirSync(path.join(process.cwd(), imgs_dir)).sort((a, b) => a.localeCompare(b, undefined, {
      numeric: true
    })) // Ensures numerical & alphabetical sorting
    .splice(1, size_of_input_data);

  const text_labels = await extractColumnFromCSV(text_dir, 3).then((columnValues) => {
    return columnValues.splice(0, size_of_input_data);
  }).catch(console.error);
  var img_files = [];
  for (var i = 0; i < imgs.length; i++) {
    img_files.push(
      (
        await sharp(path.join(process.cwd(), imgs_dir, imgs[i]))
        .resize(200, 200)
        .jpeg({
          quality: 50
        })
        .toBuffer()
      ).toString("base64")
    );
  }
  var image_embeddings = [];
  for (var i = 0; i < img_files.length; i++) {
    console.log("Getting embeddings for image " + i);
    const response = await getEmbeddings(img_files[i], 'image');
    image_embeddings.push(response);
  }
  var text_embeddings = [];
  for (var i = 0; i < text_labels.length; i++) {
    console.log("Getting embeddings for text " + i);
    const response = await getEmbeddings(text_labels[i], 'text');
    text_embeddings.push(response);
  }
  console.log("prepare data for adding data to table image")
  var data = [];
  //for image
  if (image_embeddings.length > 0) {
    for (var i = 0; i < img_files.length; i++) {
      data.push({
        img: path.join("/", "images", imgs[i]),
        vector: image_embeddings[i],
      });
    }
    await db.createTable(process.env.LANCEDB_TABLE_NAME || "table", (data = data));
  }
  //for text
  var text_data = []
  if (text_embeddings.length > 0) {
    for (var i = 0; i < img_files.length; i++) {
      text_data.push({
        img: path.join("/", "images", imgs[i]),
        vector: text_embeddings[i],
      });
    }
    await db.createTable(process.env.LANCEDB_TABLE_NAME_TEXT || "table_text", (data = text_data));
  }
  return process.env.LANCEDB_TABLE_NAME || "table";
}

async function getEmbeddings(data, type) {
  try {
    if (type === "text") {
      return await embedText(data);
    } else if (type === "image") {
      return await embedImage(data);
    } else {
      throw new Error("Invalid type. Expected 'text' or 'image'.");
    }
  } catch (error) {
    console.error("Error getting embedding:", error);
    throw error;
  }
}

async function embedText(text) {
  const response = await axios({
    method: "POST",
    url: "https://infer.roboflow.com/clip/embed_text",
    params: {
      api_key: process.env.RF_API_KEY || "",
    },
    data: {
      clip_version_id: "ViT-B-16",
      text: text,
    },
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response.data.embeddings[0];
}

async function embedImage(file) {
  const response = await axios({
    method: "POST",
    url: `https://infer.roboflow.com/clip/embed_image`,
    params: {
      api_key: process.env.RF_API_KEY || "",
    },
    data: {
      clip_version_id: "ViT-B-16",
      image: [{
        type: "base64",
        value: file,
      }, ],
    },
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response.data.embeddings[0];
}


export async function createEmbeddingsTable() {
  const LANCEDB_URI = process.env.LANCEDB_URI || "table";
  const LANCEDB_TABLE_NAME = process.env.LANCEDB_TABLE_NAME || "table";
  const LANCEDB_TABLE_NAME_TEXT = process.env.LANCEDB_TABLE_NAME_TEXT || "table_text";
  const db = await connect(LANCEDB_URI);
  const tableNames = await db.tableNames();
  console.log("table names ", tableNames);
  if (tableNames.includes(LANCEDB_TABLE_NAME)) return LANCEDB_TABLE_NAME;
  if (tableNames.includes(LANCEDB_TABLE_NAME_TEXT)) return LANCEDB_TABLE_NAME_TEXT;

  // file paths for data source
  const imgs_dir = "public/images";
  const text_dir = "src/server/dataset/labels.csv";
  return await processImgsAndText(imgs_dir, text_dir, db);
}

// Initialize DB and start server
async function startServer() {
  try {
    console.log('Starting server...');
    const table_Data = await createEmbeddingsTable();
    console.log('embeddings created successfully.');
  } catch (error) {
    console.error('Error in creating embeddings:', error);
    process.exit(1);
  }
};

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

startServer();