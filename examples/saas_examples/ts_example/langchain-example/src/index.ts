import { ChatOpenAI } from '@langchain/openai';
import { AgentExecutor, createOpenAIFunctionsAgent } from 'langchain/agents';
import { DynamicStructuredTool } from '@langchain/core/tools';
import readline from 'readline/promises';
import { stdin as input, stdout as output } from 'process';
import { LanceDB } from "@langchain/community/vectorstores/lancedb";
import { OpenAIEmbeddings } from "@langchain/openai";
import { Document } from "@langchain/core/documents";
import { ChatPromptTemplate, MessagesPlaceholder } from '@langchain/core/prompts';
import { connect } from '@lancedb/lancedb';

// Environment variables
const openAIApiKey = process.env.OPENAI_API_KEY;
const lancedbApiKey = process.env.LANCEDB_API_KEY;
const lancedbUri = process.env.LANCEDB_URI;

const OPENAI_MODEL = "gpt-4o-mini";
const EMBEDDING_MODEL = "text-embedding-3-small";

// Validation checks
if (!openAIApiKey) {
  console.error('Please set the OPENAI_API_KEY environment variable');
  process.exit(1);
}

if (!lancedbApiKey || !lancedbUri) {
  console.error('Please set the LANCEDB_API_KEY and LANCEDB_URI environment variables for LanceDB Cloud');
  process.exit(1);
}

// Types and interfaces
interface CritiqueData {
  info: string;
  actions: string;
  critique: string;
}

// Initialize OpenAI embeddings
const embeddings = new OpenAIEmbeddings({
  openAIApiKey: openAIApiKey,
  modelName: EMBEDDING_MODEL
});

/**
 * Gets or creates a vector store with the given table name
 */
async function getVectorStore(tableName: string): Promise<LanceDB> {
  try {
    const db = await connect({
      uri: lancedbUri!, 
      apiKey: lancedbApiKey!,
      region: "us-east-1"
    });

    let table;
    try {
      table = await db.openTable(tableName);
    } catch (e) {
      const embedder = embeddings.embedQuery.bind(embeddings);
      const embedding = await embedder("Initial document");
      
      table = await db.createTable(tableName, [
        { 
          vector: embedding, 
          text: "Initial document", 
          metadata: JSON.stringify({}) 
        }
      ], { mode: "overwrite" });
    }

    // Create LangChain VectorStore from the existing table
    return new LanceDB(embeddings, { table });
  } catch (error) {
    console.error(`Error connecting to LanceDB Cloud: ${error}`);
    throw error;
  }
}

/**
 * Inserts critique data into the vector store
 */
async function insertCritiques({ info, actions, critique }: CritiqueData): Promise<string> {
  try {
    const vectorStore = await getVectorStore("fitness-critiques");
    
    await vectorStore.addDocuments([
      new Document({
        pageContent: info,
        metadata: {
          actions,
          critique,
          timestamp: new Date().toISOString()
        }
      })
    ]);
    
    return 'Inserted critique into LanceDB Cloud.';
  } catch (error) {
    console.error('Error inserting critique:', error);
    return `Error inserting critique: ${error}`;
  }
}

/**
 * Retrieves similar critiques based on a query
 */
async function retrieveCritiques({ query }: { query: string }): Promise<string> {
  try {
    const vectorStore = await getVectorStore("fitness-critiques");
    const results = await vectorStore.similaritySearch(query, 5);
    
    if (results.length === 0) {
      return 'No similar critiques found in LanceDB Cloud. Continue with your analysis.';
    }
    
    const formattedResults = results.map((doc: Document) => [
      doc.metadata.actions || "No actions recorded",
      doc.metadata.critique || "No critique recorded"
    ]);
    
    return "Continue with the list with relevant actions and critiques which are in the format [[action, critique], ...]:\n" + 
           JSON.stringify(formattedResults);
  } catch (error) {
    console.error('Error retrieving critiques:', error);
    return `Error retrieving critiques: ${error}`;
  }
}

/**
 * Creates a search tool for the agent
 */
const createSearchTool = (apiKey?: string) => {
  return new DynamicStructuredTool({
    name: "search",
    description: "A search engine. Useful for when you need to answer questions about current events. Input should be a search query.",
    schema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "The search query"
        }
      },
      required: ["query"]
    },
    func: async ({ query }) => {
      if (!apiKey) {
        return "SerpAPI key not provided. Please set the SERPAPI_API_KEY environment variable.";
      }
      return `Searched for: ${query}. To implement a real search, you would need to call the SerpAPI with your key.`;
    },
  });
};

// System prompt for the agent
const SYSTEM_TEMPLATE = `
You are a fitness trainer AI assistant. 
Your goal is to provide personalized fitness advice based on the user's information and interests.

When responding to user queries, follow these steps:
1. Retrieve and review past similar actions and critiques if there are any
2. Keep these past actions and critiques in mind while researching an exercise routine
3. Before returning your final response, you MUST insert the actions you took (as a numbered list) and critiques (negative feedback, limitations, potential biases) into the database

Remember to be helpful, accurate, and considerate of the user's fitness level and goals.

The system uses:
- LangChain for agent orchestration and vector store abstraction
- LanceDB Cloud for efficient cloud-based vector storage and retrieval
- OpenAI for embeddings and LLM functionality
- JSON Schema for input validation
`;

/**
 * Main execution function
 */
async function main() {
  try {
    // Create schemas for the tools
    const insertCritiquesModel = {
      type: "object",
      properties: {
        info: {
          type: "string",
          description: "should be demographics or interests or other information about the exercise request provided by the user"
        },
        actions: {
          type: "string",
          description: "numbered list of langchain agent actions taken (searched for, gave this response, etc.)"
        },
        critique: {
          type: "string",
          description: "negative constructive feedback on the actions you took, limitations, potential biases, and more"
        }
      },
      required: ["info", "actions", "critique"]
    };

    const retrieveCritiquesModel = {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "should be demographics or interests or other information about the exercise request provided by the user"
        }
      },
      required: ["query"]
    };
    
    // Initialize OpenAI model
    const model = new ChatOpenAI({ 
      temperature: 0, 
      modelName: OPENAI_MODEL, 
      openAIApiKey: openAIApiKey 
    });
    
    // Set up SerpAPI
    const serpApiKey = process.env.SERPAPI_API_KEY;
    if (!serpApiKey) {
      console.warn('SERPAPI_API_KEY not set, SerpAPI tool may not work correctly');
    }
    
    // Configure tools
    const tools = [
      createSearchTool(serpApiKey),
      new DynamicStructuredTool({
        name: 'insert-critiques',
        description: 'Insert actions and critiques for similar exercise requests in the future.',
        schema: insertCritiquesModel,
        func: insertCritiques,
      }),
      new DynamicStructuredTool({
        name: 'retrieve-critiques',
        description: 'Retrieve actions and critiques for similar exercise requests.',
        schema: retrieveCritiquesModel,
        func: retrieveCritiques,
      }),
    ];
    
    // Create prompt template and agent
    const prompt = ChatPromptTemplate.fromMessages([
      ["system", SYSTEM_TEMPLATE],
      ["human", "{input}"],
      new MessagesPlaceholder("agent_scratchpad"),
    ]);
    
    const agent = await createOpenAIFunctionsAgent({
      llm: model,
      tools,
      prompt,
    });
    
    const executor = AgentExecutor.fromAgentAndTools({
      agent,
      tools,
      verbose: true,
    });
    
    console.log('Loaded agent. Agent will use LanceDB-LangChain integration for memory.');

    // Start interactive loop
    const rl = readline.createInterface({ input, output });
    
    while (true) {
      const query = await rl.question('Tell us about you and your fitness interests: ');
      console.log(`Executing with query '${query}'...`);
      const result = await executor.invoke({ input: query });
      console.log({ result });
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Run the main function
main().catch(console.error); 