# %% [markdown]
# # Youtube Transcript Search QA Bot
# 
# This Q&A bot will allow you to search through youtube transcripts using natural language! By going through this notebook, we'll introduce how you can use LanceDB to store and manage your data easily.

# %%
# !pip install --quiet openai datasets 
# !pip install --quiet -U lancedb

# %% [markdown]
# ## Download the data
# 
# For this dataset we're using the HuggingFace dataset `jamescalam/youtube-transcriptions`.
# 
# From the [website](https://huggingface.co/datasets/jamescalam/youtube-transcriptions):
# 
# ```
# The YouTube transcriptions dataset contains technical tutorials (currently from James Briggs, Daniel Bourke, and AI Coffee Break) transcribed using OpenAI's Whisper (large). Each row represents roughly a sentence-length chunk of text alongside the video URL and timestamp.
# ```
# 
# We'll use the training split with 700 videos and 208619 sentences

# %%
from datasets import load_dataset

data = load_dataset('jamescalam/youtube-transcriptions', split='train')
data

# %% [markdown]
# ## Prepare context
# 
# Each item in the dataset contains just a short chunk of text. We'll need to merge a bunch of these chunks together on a rolling basis. For this demo, we'll merge 20 rows and step over 4 rows at a time. LanceDB offers chaining support so you can write declarative, readable and parameterized queries. Here we serialize to Pandas as well:

# %%
from lancedb.context import contextualize

df = (contextualize(data.to_pandas())
      .groupby("title").text_col("text")
      .window(20).stride(4)
      .to_df())
df.head(1)

# %% [markdown]
# ## Create embedding function
# To create embeddings out of the text, we'll call the OpenAI embeddings API to get embeddings.
# Make sure you have an API key setup and that your account has available credits.

# %%
import openai
import os

# Configuring the environment variable OPENAI_API_KEY
if "OPENAI_API_KEY" not in os.environ:
    # OR set the key here as a variable
    openai.api_key = "sk-..."
    
assert len(openai.Model.list()["data"]) > 0

# %% [markdown]
# We'll use the ada2 text embeddings model

# %%
def embed_func(c):    
    rs = openai.Embedding.create(input=c, engine="text-embedding-ada-002")
    return [record["embedding"] for record in rs["data"]]

# %% [markdown]
# ## Create the LanceDB Table
# OpenAI API often fails or times out. So LanceDB's API provides retry and throttling features behind the scenes to make it easier to call these APIs. In LanceDB the primary abstraction you'll use to work with your data is a Table. A Table is designed to store large numbers of columns and huge quantities of data! For those interested, a LanceDB is columnar-based, and uses Lance, an open data format to store data.

# %%
import lancedb
from lancedb.embeddings import with_embeddings

data = with_embeddings(embed_func, df, show_progress=True)
data.to_pandas().head(1)

# %% [markdown]
# Now we're ready to save the data and create a new LanceDB table

# %%
# !rm -rf /tmp/lancedb

db = lancedb.connect("/tmp/lancedb")
tbl = db.create_table("chatbot", data)
len(tbl)

# %% [markdown]
# The table is backed by a Lance dataset so it's easy to integrate into other tools (e.g., pandas)

# %%
tbl.to_pandas().head(1)

# %% [markdown]
# ## Create and answer the prompt
# 
# For a given context (bunch of text), we can ask the OpenAI Completion API to answer an arbitrary question using the following prompt:

# %%
def create_prompt(query, context):
    limit = 3750

    prompt_start = (
        "Answer the question based on the context below.\n\n"+
        "Context:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {query}\nAnswer:"
    )
    # append contexts until hitting limit
    for i in range(1, len(context)):
        if len("\n\n---\n\n".join(context.text[:i])) >= limit:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(context.text[:i-1]) +
                prompt_end
            )
            break
        elif i == len(context)-1:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(context.text) +
                prompt_end
            )    
    return prompt

# %%
def complete(prompt):
    # query text-davinci-003
    res = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=0,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return res['choices'][0]['text'].strip()

# check that it works
query = "who was the 12th person on the moon and when did they land?"
complete(query)

# %% [markdown]
# ## Let's put it all together now

# %%
query = ("Which training method should I use for sentence transformers "
         "when I only have pairs of related sentences?")

# %%
# Embed the question
emb = embed_func(query)[0]

# %% [markdown]
# 
# Again we'll use LanceDB's chaining query API. This time, we'll perform similarity search to find similar embeddings to our query. We can easily tweak the parameters in the query to produce the best result.

# %%
# Use LanceDB to get top 3 most relevant context
context = tbl.search(emb).limit(3).to_df()

# %%
# Get the answer from completion API
prompt = create_prompt(query, context)
complete(prompt)

# %%
from IPython.display import YouTubeVideo

top_match = context.iloc[0]
YouTubeVideo(top_match["url"].split("/")[-1], start=int(top_match["start"]))

# %%



