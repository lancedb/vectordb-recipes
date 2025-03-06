// External imports
import { connect, Index, Table } from '@lancedb/lancedb';
import { FixedSizeList, Field, Float32, Schema, Utf8 } from 'apache-arrow';
import { pipeline } from '@xenova/transformers';
import * as dotenv from 'dotenv';

// Load environment variables
dotenv.config();

// Type definitions
interface Document {
    text: string;
    label: number;
    embedding?: number[];
    [key: string]: unknown;
}

interface AGNewsSearchResult {
    text: string;
    label: number;
    _distance: number;
}

interface HfDatasetResponse {
    rows: {
        row: {
            text: string;
            label: number;
        };
    }[];
}

// Constants
const BATCH_SIZE = 100; // HF API default limit
const POLL_INTERVAL = 10000; // 10 seconds
const EMBEDDING_DIM = 384;
const MODEL_NAME = 'Xenova/all-MiniLM-L6-v2';

/**
 * Loads documents from the Hugging Face dataset API in batches
 */
async function loadDataset(datasetName: string, split: string = 'train', targetSize: number = 1000): Promise<Document[]> {    
    try {
        console.log('Fetching dataset...');
        const batches = Math.ceil(targetSize / BATCH_SIZE);
        let allDocuments: Document[] = [];

        for (let i = 0; i < batches; i++) {
            const offset = i * BATCH_SIZE;
            const url = `https://datasets-server.huggingface.co/rows?dataset=${datasetName}&config=default&split=${split}&offset=${offset}&limit=${BATCH_SIZE}`;
            console.log(`Fetching batch ${i + 1}/${batches} from offset ${offset}...`);
            
            const response = await fetch(url);
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error response:', errorText);
                throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
            }
            
            const data = JSON.parse(await response.text()) as HfDatasetResponse;
            if (!data.rows) {
                throw new Error('No rows found in response');
            }
            
            console.log(`Received ${data.rows.length} rows in batch ${i + 1}`);
            const documents = data.rows.map(({ row }) => ({
                text: row.text,
                label: row.label
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

/**
 * Generates embeddings for the given texts using the Xenova transformer model
 */
async function generateEmbeddings(texts: string[]): Promise<number[][]> {
    const embedder = await pipeline('feature-extraction', MODEL_NAME);
    const embeddings = await Promise.all(
        texts.map(async (text) => {
            const embedding = await embedder(text, { pooling: 'mean', normalize: true });
            return Array.from(embedding.data);
        })
    );
    return embeddings;
}

/**
 * Main execution function
 */
async function main() {
    try {
        // Step 1: Load the AG News dataset
        console.log('Loading AG News dataset...');
        const datasetName = "fancyzhx/ag_news";
        const sampleData = await loadDataset(datasetName);
        console.log(`Loaded ${sampleData.length} examples from AG News dataset`);

        // Step 2: Generate embeddings for the loaded data
        console.log('Generating embeddings...');
        const rawEmbeddings = await generateEmbeddings(sampleData.map(doc => doc.text));
        const dataWithEmbeddings = sampleData.map((doc, i) => ({
            ...doc,
            embedding: rawEmbeddings[i]
        }));

        // Step 3: Connect to LanceDB and create table
        const dbUri = process.env.LANCEDB_URI || 'db://your-database-uri';
        const apiKey = process.env.LANCEDB_API_KEY;
        const db = await connect(dbUri, { apiKey });
        const tableName = "lancedb-cloud-quickstart";

        // Create schema with vector dimension
        const schema = new Schema([
            new Field('text', new Utf8(), true),
            new Field('label', new Float32(), true),
            new Field('embedding', new FixedSizeList(EMBEDDING_DIM, new Field('item', new Float32(), true)), true)
        ]);

        // Create table with explicit schema
        const table = await db.createTable(tableName, dataWithEmbeddings, { 
            schema,
            mode: "overwrite" 
        });
        console.log('Successfully created table');

        // Step 4: Create and wait for index
        await table.createIndex("embedding", {
            config: Index.ivfPq({
                distanceType: "cosine",
            }),
        });

        const indexName = "embedding_idx";
        await waitForIndex(table, indexName);
        console.log(await table.indexStats(indexName));

        // Step 5: Perform semantic search with example query
        const queryText = "Texas' Johnson, Benson Go Out With Win (AP) AP - Their final games will be remembered for the plays others made. Still, Texas tailback Cedric Benson and linebacker Derrick Johnson went out the way they wanted to: with a Rose Bowl win.";
        
        console.log('\nGenerating embedding for query...');
        const queryRawEmbedding = (await generateEmbeddings([queryText]))[0];
        
        console.log('\nSearching for similar articles...');
        const results = await table.search(queryRawEmbedding)
            .limit(5)
            .select(['text', 'label'])
            .toArray() as AGNewsSearchResult[];

        console.log('Search Results:');
        results.forEach((result, index) => {
            console.log(`\n${index + 1}. Score: ${result._distance}`);
            console.log(`Text: ${result.text}`);
            console.log(`Label: ${result.label}`);
        });

    } catch (error) {
        console.error('Error in main:', error);
    }
}

// Execute main function
main().catch(console.error); 