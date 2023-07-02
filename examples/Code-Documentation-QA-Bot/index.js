import { LanceDB } from "langchain/vectorstores/lancedb";
import { RetrievalQAChain } from "langchain/chains";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { UnstructuredLoader } from "langchain/document_loaders/fs/unstructured";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";
import { OpenAI } from "langchain/llms/openai";
import fs from 'fs';
import * as path from "node:path";
import { download } from '@guoyunhe/downloader';
import { connect } from "vectordb";


async function download_data(){
    const res = await download("https://eto-public.s3.us-west-2.amazonaws.com/datasets/pandas_docs/pandas.documentation.zip", "pandas_docs", { extract: true })
  };
  
function get_document_title(document) {
  const source = document.metadata.source;
  const regex = /pandas.documentation(.*).html/;
  const title = regex.exec(source);
  if (source | title) {
    console.log("title", title[1]);
    console.log("source", source);
  }
  return title | "";
}

async function read_data(){
  var docs = [];
  const docsPath = "pandas_docs/pandas.documentation"
  const options = {
    apiKey: "bbIkFRMzIT8M7ZMatjQIiVL8RjyYM7",
  };
  
  console.log("fs.existsSync(docsPath)", fs.existsSync(docsPath))
  if (fs.existsSync(docsPath)) {
    for (const p of fs.readdirSync(docsPath).filter((f) => f.endsWith('.html'))) {
      const docPath = path.join(docsPath, p);
      console.log(docPath);
      var rawDocument;
      try {
        const loader = new UnstructuredLoader(docPath, options);
        rawDocument = await loader.load();

      } catch (e) {
        console.log('Error loading document:', e);
        continue;
      }
      const metadata = {
        title: get_document_title(rawDocument[0]),
        version: '2.0rc0',
      };
      rawDocument[0].metadata = Object.assign(rawDocument[0].metadata, metadata);
      rawDocument[0].metadata['source'] = JSON.stringify(rawDocument[0].metadata['source']);
      docs = docs.concat(rawDocument);
    }
    
  }
  return docs;
}


(async () => {
  const apiKey = process.env.OPENAI_API_KEY
  if (apiKey == null || apiKey == undefined) {
    throw new Error("You need to provide an OpenAI API key, here we read it from the OPENAI_API_KEY environment variable")
  }

  const db = await connect("data/sample-lancedb")

  await download_data();
  var docs = await read_data();
  //make table here
  const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 1000,
      chunkOverlap: 200,
    });
  docs = await splitter.splitDocuments(docs);
  const embeddings = new OpenAIEmbeddings();
  const table = await db.createTable("vectors", [
    { vector: await embeddings.embedQuery("Hello world"), text: "sample", id: "a" },
  ]);
  const vectorStore = await LanceDB.fromDocuments(
    docs,
    embeddings,
    { table }
  );
  const chain = RetrievalQAChain.fromLLM(new OpenAI({}), vectorStore.asRetriever());
  const res = await chain.call({
    query: "How do I make use of installing optional dependencies?",
  });
  console.log({ res });
 
  // get zip file, extract, make metadata, something about splitters, emebeddings, etc.
  // then make table, query, result.

})();