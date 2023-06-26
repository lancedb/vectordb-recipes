# %% [markdown]
# # Code documentation Q&A bot example with LangChain
# 
# This Q&A bot will allow you to query your own documentation easily using questions. We'll also demonstrate the use of LangChain and LanceDB using the OpenAI API. 
# 
# In this example we'll use Pandas 2.0 documentation, but, this could be replaced for your own docs as well

# %%
# !pip install --quiet openai langchain$
# !pip install --quiet -U lancedb

# %% [markdown]
# First, let's get some setup out of the way. As we're using the OpenAI API, ensure that you've set your key (and organization if needed):

# %%
import openai
import os

# Configuring the environment variable OPENAI_API_KEY
if "OPENAI_API_KEY" not in os.environ:
    # OR set the key here as a variable
    openai.api_key = "sk-..."
    
assert len(openai.Model.list()["data"]) > 0

# %% [markdown]
# # Loading in our code documentation, generating embeddings and storing our documents in LanceDB
# 
# We're going to use the power of LangChain to help us create our Q&A bot. It comes with several APIs that can make our development much easier as well as a LanceDB integration for vectorstore.

# %%
import lancedb
import re
import pickle
import requests
import zipfile
from pathlib import Path

from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import LanceDB
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# %% [markdown]
# To make this easier, we've downloaded Pandas documentation and stored the raw HTML files for you to download. We'll download them and then use LangChain's HTML document readers to parse them and store them in LanceDB as a vector store, along with relevant metadata.

# %%
pandas_docs = requests.get("https://eto-public.s3.us-west-2.amazonaws.com/datasets/pandas_docs/pandas.documentation.zip")
with open('/tmp/pandas.documentation.zip', 'wb') as f:
    f.write(pandas_docs.content)

file = zipfile.ZipFile("/tmp/pandas.documentation.zip")
file.extractall(path="/tmp/pandas_docs")

# %% [markdown]
# We'll create a simple helper function that can help to extract metadata, so we can use this downstream when we're wanting to query with filters. In this case, we want to keep the lineage of the uri or path for each document that we process:

# %%
def get_document_title(document):
    m = str(document.metadata["source"])
    title = re.findall("pandas.documentation(.*).html", m)
    if title[0] is not None:
        return(title[0])
    return ''

# %% [markdown]
# # Pre-processing and loading the documentation
# 
# Next, let's pre-process and load the documentation. To make sure we don't need to do this repeatedly if we were updating code, we're caching it using pickle so we can retrieve it again (this could take a few minutes to run the first time yyou do it). We'll also add some more metadata to the docs here such as the title and version of the code:

# %%
docs_path = Path("docs.pkl")
docs = []

if not docs_path.exists():
    for p in Path("/tmp/pandas_docs/pandas.documentation").rglob("*.html"):
        print(p)
        if p.is_dir():
            continue
        loader = UnstructuredHTMLLoader(p)
        raw_document = loader.load()
        
        m = {}
        m["title"] = get_document_title(raw_document[0])
        m["version"] = "2.0rc0"
        raw_document[0].metadata = raw_document[0].metadata | m
        raw_document[0].metadata["source"] = str(raw_document[0].metadata["source"])
        docs = docs + raw_document

    with docs_path.open("wb") as fh:
        pickle.dump(docs, fh)
else:
    with docs_path.open("rb") as fh:
        docs = pickle.load(fh)

# %% [markdown]
# # Generating emebeddings from our docs
# 
# Now that we have our raw documents loaded, we need to pre-process them to generate embeddings:

# %%
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
documents = text_splitter.split_documents(docs)
embeddings = OpenAIEmbeddings()

# %% [markdown]
# # Storing and querying with LanceDB
# 
# Let's connect to LanceDB so we can store our documents. We'll create a Table to store them in:

# %%
db = lancedb.connect('/tmp/lancedb')
table = db.create_table("pandas_docs", data=[
    {"vector": embeddings.embed_query("Hello World"), "text": "Hello World", "id": "1"}
], mode="overwrite")
docsearch = LanceDB.from_documents(documents, embeddings, connection=table)

# %% [markdown]
# Now let's create our RetrievalQA chain using the LanceDB vector store:

# %%
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())

# %% [markdown]
# And thats it! We're all setup. The next step is to run some queries, let's try a few:

# %%
query = "What are the major differences in pandas 2.0?"
qa.run(query)

# %%
query = "What's the current version of pandas?"
qa.run(query)

# %%
query = "How do I make use of installing optional dependencies?"
qa.run(query)

# %%
query = "What are the backwards incompatible API changes in Pandas 2.0?"
qa.run(query)

# %%



