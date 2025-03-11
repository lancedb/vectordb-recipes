import { connect, Index, Table } from '@lancedb/lancedb';
import { FixedSizeList, Field, Float32, Schema, Utf8 } from 'apache-arrow';
import * as dotenv from 'dotenv';

// Load environment variables
dotenv.config();

// Type definitions
interface Document {
    text: string;
    label: number;
    keywords: string[];
    // embedding?: number[];
    embeddings?: number[];
    [key: string]: unknown;
}

interface HfDatasetResponse {
    rows: {
        row: {
            text: string;
            label: number;
            keywords: string[];
            keywords_embeddings?: number[];
        };
    }[];
}

// Constants
const BATCH_SIZE = 100; // HF API default limit
const POLL_INTERVAL = 10000; // 10 seconds
const MAX_RETRIES = 5;
const INITIAL_RETRY_DELAY = 1000; // 1 second

/**
 * Loads documents from the Hugging Face dataset API in batches
 */
async function loadDataset(datasetName: string, split: string = 'train', targetSize: number = 1000, offset: number = 0): Promise<Document[]> {    
    try {
        console.log('Fetching dataset...');
        const batches = Math.ceil(targetSize / BATCH_SIZE);
        let allDocuments: Document[] = [];
        const hfToken = process.env.HF_TOKEN; // Optional Hugging Face token

        for (let i = 0; i < batches; i++) {
            const offset = i * BATCH_SIZE;
            const url = `https://datasets-server.huggingface.co/rows?dataset=${datasetName}&config=default&split=${split}&offset=${offset}&limit=${BATCH_SIZE}`;
            console.log(`Fetching batch ${i + 1}/${batches} from offset ${offset}...`);
            
            // Add retry logic with exponential backoff
            let retries = 0;
            let success = false;
            let data: HfDatasetResponse | null = null;

            while (!success && retries < MAX_RETRIES) {
                try {
                    const headers: HeadersInit = {
                        'Content-Type': 'application/json',
                    };
                    
                    // Add authorization header if token is available
                    if (hfToken) {
                        headers['Authorization'] = `Bearer ${hfToken}`;
                    }
                    
                    const fetchOptions = {
                        method: 'GET',
                        headers,
                        timeout: 30000, // 30 second timeout
                    };
                    
                    const response = await fetch(url, fetchOptions);
                    if (!response.ok) {
                        const errorText = await response.text();
                        console.error(`Error response (attempt ${retries + 1}):`, errorText);
                        throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
                    }
                    
                    data = JSON.parse(await response.text()) as HfDatasetResponse;
                    if (!data.rows) {
                        throw new Error('No rows found in response');
                    }
                    
                    success = true;
                } catch (error) {
                    retries++;
                    if (retries >= MAX_RETRIES) {
                        console.error(`Failed after ${MAX_RETRIES} retries:`, error);
                        throw error;
                    }
                    
                    const delay = INITIAL_RETRY_DELAY * Math.pow(2, retries - 1);
                    console.log(`Retry ${retries}/${MAX_RETRIES} after ${delay}ms...`);
                    await new Promise(resolve => setTimeout(resolve, delay));
                }
            }
            
            // Ensure data is defined before using it
            if (!data || !data.rows) {
                throw new Error('No data received after retries');
            }
            
            console.log(`Received ${data.rows.length} rows in batch ${i + 1}`);
            const documents = data.rows.map(({ row }) => ({
                text: row.text,
                label: row.label,
                keywords: row.keywords,
                embeddings: row.keywords_embeddings
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
 * Main execution function
 */
async function main() {
    try {
        // Step 1: Connect to LanceDB
        const dbUri = process.env.LANCEDB_URI || 'db://your-database-uri';
        const apiKey = process.env.LANCEDB_API_KEY;
        const db = await connect(dbUri, { apiKey });
        const tableName = "lancedb-cloud-quickstart";

        // Step 2: Load the AG News dataset 
        console.log('Loading AG News dataset...');
        const datasetName = "sunhaozhepy/ag_news_sbert_keywords_embeddings";
        const split = "test";
        const targetSize = 1000;
        const sampleData = await loadDataset(datasetName, split, targetSize);
        console.log(`Loaded ${sampleData.length} examples from AG News dataset`);


        const dataWithEmbeddings: Document[] = sampleData;
        // Get embedding dimension from the first document with an embedding
        const firstDocWithEmbedding = dataWithEmbeddings.find((doc: Document) => 
            (doc.embeddings && Array.isArray(doc.embeddings) && doc.embeddings.length > 0));
            
        if (!firstDocWithEmbedding || !firstDocWithEmbedding.embeddings || !Array.isArray(firstDocWithEmbedding.embeddings)) {
            throw new Error('No document with valid embeddings found in the dataset. Please check if keywords_embeddings field exists.');
        }
        const embeddingDimension = firstDocWithEmbedding.embeddings.length;

        // Create schema
        const schema = new Schema([
            new Field('text', new Utf8(), true),
            new Field('label', new Float32(), true),
            new Field('keywords', new Utf8(), true),
            new Field('embeddings', new FixedSizeList(embeddingDimension, new Field('item', new Float32(), true)), true)
        ]);

        // Step 3: Create table with data
        const table = await db.createTable(tableName, dataWithEmbeddings, { 
            schema,
            mode: "overwrite" 
        });
        console.log('Successfully created table');

        // Step 4: Create and wait for index
        await table.createIndex("embeddings", {
            config: Index.ivfPq({
                distanceType: "cosine",
            }),
        });

        const indexName = "embeddings_idx";
        await waitForIndex(table, indexName);
        console.log(await table.indexStats(indexName));        

        // Step 5: Perform semantic search with example query
        const queryDocs = await loadDataset(datasetName, split, 1, targetSize);
        if (queryDocs.length === 0) {
            throw new Error("Failed to load a query document");
        }
        const queryDoc = queryDocs[0];
        if (!queryDoc.embeddings || !Array.isArray(queryDoc.embeddings)) {
            throw new Error("Query document doesn't have a valid embedding after processing");
        }
        const results = await table.search(queryDoc.embeddings)
            .limit(5)
            .select(['text','keywords','label'])
            .toArray();

        console.log('Search Results:');
        results.forEach((result, index) => {
            console.log(`\n${index + 1}. Score: ${result._distance}`);
            console.log(`Text: ${result.text}`);
            console.log(`Keywords: ${result.keywords}`);
            console.log(`Label: ${result.label}`);
        });

        // perform semantic search with a filter applied
        const filteredResultsesults = await table.search(queryDoc.embeddings)
            .where("label > 2")
            .limit(5)
            .select(['text', 'keywords','label'])
            .toArray();

        console.log('Search Results with filter:');
        filteredResultsesults.forEach((result, index) => {
            console.log(`\n${index + 1}. Score: ${result._distance}`);
            console.log(`Text: ${result.text}`);
            console.log(`Keywords: ${result.keywords}`);
            console.log(`Label: ${result.label}`);
        });

    } catch (error) {
        console.error('Error in main:', error);
    }
}

// Execute main function
main().catch(console.error); 