# Agent memory over a markdown vault with LanceDB

Give a coding agent a searchable memory of your notes: an Obsidian vault, a `docs/` folder, or any directory of
`.md` files. The agent asks "what did we decide about pricing?" and gets the right notes back, from a single
embedded LanceDB table that sits next to the notes.

One file (`main.py`), no server, no API key. Embeddings run locally with `multilingual-e5-small`, so notes in
other languages work too.

## What it shows

- **Embedded LanceDB as a memory store**: one directory, `<vault>/.lancedb-memory/`, that syncs like any other folder.
- **Explicit Arrow schema** with a fixed-size vector column and metadata columns (`path`, `scope`, `title`, `text`).
- **Incremental indexing**: each note is hashed; unchanged notes are skipped, edited notes are replaced
  (`table.delete` + `table.add`), notes removed from the vault leave the memory.
- **Prefiltered search**: `--scope decisions` restricts the search to one top-level folder with
  `.where(..., prefilter=True)`, so the filter is applied before the nearest-neighbour search.
- **Cosine metric** with e5-style `query:` / `passage:` prefixes.

## Run it

```bash
cd examples/agent-memory-markdown-vault
pip install -r requirements.txt

python main.py index sample_vault              # first run downloads the embedding model
python main.py recall sample_vault "what did we decide about pricing"
python main.py recall sample_vault "who handles invoices" -n 3
python main.py recall sample_vault "pricing" --scope people     # same query, other folder
```

Point it at your own notes by replacing `sample_vault` with any directory. Re-run `index` whenever notes change;
only the changed notes are re-embedded. Embedding happens before the table is touched, so a failed run leaves the
previous memory intact. Run one `index` at a time per vault (there is no write lock).

## Use it from an agent

`recall` prints plain text, so any agent that can run a shell command can use it:

```bash
python main.py recall ~/MyVault "<what the agent needs to remember>" -n 5
```

For an HTTP endpoint or an MCP tool on top of the same idea (plus a cross-encoder reranker and other vector
backends), see [vault-recall](https://github.com/tonydzi/vault-recall), where the LanceDB backend in this recipe
comes from.

## How it works

1. `read_notes` walks the vault, strips YAML frontmatter, and records the top-level folder as `scope`.
2. `chunk` splits on headings and blank lines and packs paragraphs into chunks of about 1200 characters.
3. `index` embeds the chunks of new or changed notes and writes them to the `notes` table.
4. `recall` embeds the query, searches the table with the cosine metric, optionally prefiltered by `scope`, and
   prints the best chunks with their score and file path.

Embedding model: [`intfloat/multilingual-e5-small`](https://huggingface.co/intfloat/multilingual-e5-small)
(384 dimensions). To use another model, change `EMBED_MODEL` and `DIM` in `main.py`.
