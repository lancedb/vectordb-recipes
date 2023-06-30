const lancedb = require('vectordb')
const { Configuration, OpenAIApi } = require('openai')
const { stdin: input, stdout: output } = require('process')


(async () => {
  const apiKey = process.env.OPENAI_API_KEY
  if (apiKey == null || apiKey == undefined) {
    throw new Error("You need to provide an OpenAI API key, here we read it from the OPENAI_API_KEY environment variable")
  }

  const embedFunction = new lancedb.OpenAIEmbeddingFunction('context', apiKey)

  const db = await lancedb.connect("data/sample-lancedb")

  //make table here


  const configuration = new Configuration({ apiKey })
  const openai = new OpenAIApi(configuration)

  // get zip file, extract, make metadata, something about splitters, emebeddings, etc.
  // then make table, query, result.

})();