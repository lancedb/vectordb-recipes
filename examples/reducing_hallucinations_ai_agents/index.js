const { z } = require('zod')
const { ChatOpenAI } = require('langchain/chat_models/openai')
const { initializeAgentExecutorWithOptions } = require('langchain/agents')
const { DynamicStructuredTool, SerpAPI } = require('langchain/tools')
const readline = require('readline/promises')
const { stdin: input, stdout: output } = require('process')
const lancedb = require('vectordb')

// You need to provide an OpenAI API key, here we read it from the OPENAI_API_KEY environment variable
const apiKey = process.env.OPENAI_API_KEY
// The embedding function will create embeddings for the 'info' column
const embedFunction = new lancedb.OpenAIEmbeddingFunction('info', apiKey)

async function insertCritiques({ info, actions, critique }) {
  const db = await lancedb.connect('data/agent-lancedb')

  // Open the fitness-routine table or create one if it does not exist, then insert
  const tableName = 'fitness-routine'
  if ((await db.tableNames()).includes(tableName)) {
    const tbl = await db.openTable(tableName, embedFunction)
    tbl.add([{ info, actions, critique }])
  } else {
    console.log({ info, actions, critique })
    await db.createTable(tableName, [{ info, actions, critique }], 'create', embedFunction)
  }
  return 'Inserted and done.'
}

async function retrieveCritiques({ query }) {
  const db = await lancedb.connect('data/agent-lancedb')

  // Retrieve if fitness-routine table exists
  const tableName = 'fitness-routine'
  if ((await db.tableNames()).includes(tableName)) {
    const tbl = await db.openTable(tableName, embedFunction)
    const results = await tbl.search(query).limit(5).select(['actions', 'critique']).execute()
    const formattedResults = JSON.stringify(results.map(r => [r.actions, r.critique]))
    return "Continue with the list with relevant actions and critiques which are in the format [[action, critique], ...]:\n" + formattedResults
  } else {
    return 'No info but continue.'
  }
}

// prompt engineering
function createPrompt(info) {
  const promptStart = (
      'Please execute actions as a fitness trainer based on the information about the user and their interests below.\n\n'+
      'Info from the user:\n\n'
  )
  const promptEnd = (
      '\n\n1. Retrieve using user info and review the past actions and critiques if there is any\n'+
      '2. Keep past actions and critiques in mind while researching for an exercise routine with steps which we respond to the user\n'+
      '3. Before returning the response, it is of upmost importance to insert the actions you took (numbered list: searched for, found this, etc.) and critiques (negative feedback: limitations, potential biases, and more) into the database for getting better exercise routines in the future. \n'
  )

  return promptStart + info + promptEnd
}

(async () => {
  // create insert critiques schema
  const insertCritiquesModel = z.object({
    info: z.string().describe('should be demographics or interests or other information about the exercise request provided by the user'),
    actions: z.string().describe('numbered list of langchain agent actions taken (searched for, gave this response, etc.)'),
    critique: z.string().describe('negative constructive feedback on the actions you took, limitations, potential biases, and more')
  })

  // create retrieve critiques schema
  const retrieveCritiquesModel = z.object({
    query: z.string().describe('should be demographics or interests or other information about the exercise request provided by the user'),
  })
  
  // set up langchain tools and llm
  const model = new ChatOpenAI({ temperature: 0, model: 'gpt-3.5-turbo-0613' })
  const tools = [
    // you must have SERPAPI_API_KEY environment set
    new SerpAPI(),
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
  ]

  // create agent
  const executor = await initializeAgentExecutorWithOptions(tools, model, {
    agentType: 'structured-chat-zero-shot-react-description',
    verbose: true,
  })
  console.log('Loaded agent.')

  const rl = readline.createInterface({ input, output })
  while (true) {
    // ask for user info
    const query = await rl.question('Tell us about you and your fitness interests: ')
  
    console.log(`Executing with query '${query}'...`)

    // run agent
    const result = await executor.call({ input: createPrompt(query) })
  
    console.log({ result })
  }
})()