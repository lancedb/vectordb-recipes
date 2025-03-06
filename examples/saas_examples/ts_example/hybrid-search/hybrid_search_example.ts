import { connect, embedding, rerankers, Index, Table } from '@lancedb/lancedb';
import "@lancedb/lancedb/embedding/openai";
import { Utf8, Int32 } from 'apache-arrow';
import * as dotenv from 'dotenv';

// Load environment variables
dotenv.config();

// Constants
const POLL_INTERVAL = 5000; // 5 seconds
const DATASET_NAME = 'BeIR/scidocs';
const BATCH_SIZE = 100; // HF API default limit

interface Document {
  _id: string;
  title: string;
  text: string;
  vector: number[];
  _distance?: number;
}

interface HfDatasetResponse {
  rows: {
    row: {
      _id: string;
      title: string;
      text: string;
    };
  }[];
}

/**
 * Loads documents from the BeIR/scidocs dataset in batches
 */
async function loadDataset(split: string = 'corpus', targetSize: number = 100): Promise<Document[]> {    
  try {
    console.log('Fetching BeIR/scidocs dataset...');
    const batches = Math.ceil(targetSize / BATCH_SIZE);
    let allDocuments: Document[] = [];

    for (let i = 0; i < batches; i++) {
      const offset = i * BATCH_SIZE;
      const url = `https://datasets-server.huggingface.co/rows?dataset=${DATASET_NAME}&config=corpus&split=corpus&offset=${offset}&limit=${BATCH_SIZE}`;
      console.log(`Fetching batch ${i + 1}/${batches} from offset ${offset}...`);
      
      const response = await fetch(url);
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error response:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
      }
      
      const data = JSON.parse(await response.text()) as HfDatasetResponse;
      if (!data.rows || data.rows.length === 0) {
        throw new Error('No rows found in response');
      }
      
      console.log(`Received ${data.rows.length} rows in batch ${i + 1}`);
      const documents = data.rows.map(({ row }) => ({
        _id: row._id,
        title: row.title,
        text: row.text,
        vector: []
      }));
      allDocuments = allDocuments.concat(documents);
      
      if (data.rows.length < BATCH_SIZE) {
        console.log('Reached end of dataset');
        break;
      }
    }

    console.log(`Total documents loaded: ${allDocuments.length}`);
    return allDocuments;
  } catch (error) {
    console.error("Failed to load dataset:", error);
    throw error;
  }
}

/**
 * Waits for the LanceDB index to be ready
 */
async function waitForIndex(table: Table, indexName: string): Promise<void> {
  while (true) {
      const indices = await table.listIndices();
      if (indices.some((index) => index.name === indexName)) {
          break; 
      }
      console.log(`⏳ Waiting for ${indexName} to be ready...`);
      await new Promise(resolve => setTimeout(resolve, POLL_INTERVAL));
  }
  console.log(`✅ ${indexName} is ready!`);
}


async function main() {
  try {
    // Initialize embedding function
    const embedFunc = embedding.getRegistry().get("openai")?.create({
      model: "text-embedding-ada-002",
    }) as embedding.EmbeddingFunction;

    const documentSchema = embedding.LanceSchema({
      title: new Utf8(),
      text: embedFunc.sourceField(new Utf8()),
      vector: embedFunc.vectorField(),
      num_words: new Int32()
    });

    const dbUri = process.env.LANCEDB_URI || 'db://your-database-uri';
    const apiKey = process.env.LANCEDB_API_KEY;
    const db = await connect(dbUri, { apiKey });

    const tableName = "hybrid_search_example";

    const table = await db.createEmptyTable(tableName, documentSchema, {
      mode: "overwrite",
    });

    const documents = await loadDataset('corpus', 100);
    console.log('Loaded documents from BeIR/scidocs dataset');
    console.log(`Total documents loaded: ${documents.length}`);

    const data = documents.map(doc => ({
      title: doc.title,
      text: doc.text,
      num_words: doc.text.split(/\s+/).length,
    }));
    
    await table.add(data);
    console.log('Successfully added documents to table');

    await table.createIndex("text", {
      config: Index.fts(),
    });
    const indexName = "text_idx";
    await waitForIndex(table, indexName);
    console.log("Created FTS index");
    console.log(await table.listIndices());
    console.log(await table.indexStats(indexName));

    const query = "What are the applications of machine learning in healthcare?";
    console.log("\nExecuting search with query:", query);
    
    console.log("\nExecuting FTS search...");
    const ftsResults = await table.query()
      .fullTextSearch(query)
      .select(["title"])
      .limit(10)
      .toArray();
    console.log("FTS results:", ftsResults);

    console.log("\nExecuting vector search...");
    const queryVector = await embedFunc.computeQueryEmbeddings(query);
    const vectorResults = await table.query()
      .nearestTo(queryVector)
      .select(["title"])
      .limit(10)
      .toArray();
    console.log("Vector results:", vectorResults);

    console.log("\nExecuting hybrid search...");
    const hybridResults = await table.query()
      .fullTextSearch(query)
      .nearestTo(queryVector)
      .rerank(await rerankers.RRFReranker.create())
      .select(["title", "text", "num_words"])
      .limit(10)
      .toArray();
    console.log("Hybrid search results:", hybridResults);

    process.exit(0);
  } catch (error) {
    console.error('Error in hybrid search example:', error);
    process.exit(1);
  }
}

main().catch(console.error); 