"""Agent memory over a folder of markdown notes, stored in LanceDB.

    python main.py index  sample_vault            # embed notes (incremental: only changed notes are re-embedded)
    python main.py recall sample_vault "what did we decide about pricing" --scope decisions
    python main.py recall sample_vault "who handles invoices" -n 3

The LanceDB table lives in <vault>/.lancedb-memory/ so the memory travels with the notes.
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

import lancedb
import pyarrow as pa
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "intfloat/multilingual-e5-small"  # 384 dims, ~470 MB, runs on CPU
TABLE = "notes"
DIM = 384
CHUNK_CHARS = 1200
SKIP_DIRS = {".git", ".obsidian", ".trash", ".lancedb-memory"}

SCHEMA = pa.schema([
    pa.field("vector", pa.list_(pa.float32(), DIM)),
    pa.field("path", pa.string()),
    pa.field("scope", pa.string()),      # top-level folder: decisions, people, projects, ...
    pa.field("title", pa.string()),
    pa.field("text", pa.string()),
    pa.field("note_hash", pa.string()),  # hash of the whole note, drives incremental indexing
])

_model = None


def model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def embed(texts, kind):
    # e5 models expect "query: " / "passage: " prefixes
    prefix = "query: " if kind == "query" else "passage: "
    vecs = model().encode([prefix + t for t in texts], normalize_embeddings=True)
    return [v.astype("float32").tolist() for v in vecs]


def chunk(body):
    """Split on headings and blank lines, then pack paragraphs up to CHUNK_CHARS."""
    chunks, cur = [], ""
    for block in re.split(r"\n(?=#{1,6}\s)|\n\s*\n", body.strip()):
        block = block.strip()
        if not block:
            continue
        if cur and len(cur) + len(block) + 2 > CHUNK_CHARS:
            chunks.append(cur)
            cur = block
        else:
            cur = f"{cur}\n\n{block}" if cur else block
    if cur:
        chunks.append(cur)
    return chunks


def read_notes(vault):
    for path in sorted(vault.rglob("*.md")):
        rel = path.relative_to(vault)
        if any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, flags=re.S)  # drop frontmatter
        scope = rel.parts[0] if len(rel.parts) > 1 else ""
        yield rel.as_posix(), scope, path.stem, text


def open_table(vault):
    db = lancedb.connect(str(vault / ".lancedb-memory"))
    return db.create_table(TABLE, schema=SCHEMA, exist_ok=True)  # opens the table if it already exists


def index(vault):
    table = open_table(vault)
    known = {}  # path -> note_hash already stored
    if table.count_rows():
        for r in table.search().select(["path", "note_hash"]).limit(table.count_rows()).to_list():
            known[r["path"]] = r["note_hash"]

    seen, stale, rows = set(), set(), []
    for rel, scope, title, text in read_notes(vault):
        seen.add(rel)
        note_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if known.get(rel) == note_hash:
            continue
        stale.add(rel)  # new, edited or now empty: its old rows must go
        pieces = chunk(text)
        for piece, vec in zip(pieces, embed(pieces, "passage") if pieces else []):
            rows.append({"vector": vec, "path": rel, "scope": scope, "title": title,
                         "text": piece, "note_hash": note_hash})

    # embedding is done: only now touch the table, so a failed embed never loses the old memory
    stale |= set(known) - seen  # notes deleted from the vault leave the memory too
    for rel in stale:
        table.delete(f"path = '{rel.replace(chr(39), chr(39) * 2)}'")
    if rows:
        table.add(rows)
    print(f"indexed {len({r['path'] for r in rows})} changed notes, {len(rows)} chunks; "
          f"table now has {table.count_rows()} chunks")


def recall(vault, query, n=5, scope=None):
    table = open_table(vault)
    if not table.count_rows():
        sys.exit("empty memory: run `index` first")
    q = table.search(embed([query], "query")[0]).metric("cosine")
    if scope:
        q = q.where(f"scope = '{scope.replace(chr(39), chr(39) * 2)}'", prefilter=True)
    for rank, hit in enumerate(q.limit(n).to_list(), 1):
        snippet = " ".join(hit["text"].split())[:160]
        print(f"{rank}. [{1 - hit['_distance']:.3f}] {hit['path']}\n   {snippet}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("index")
    p.add_argument("vault", type=Path)
    p = sub.add_parser("recall")
    p.add_argument("vault", type=Path)
    p.add_argument("query")
    p.add_argument("-n", type=int, default=5)
    p.add_argument("--scope", help="restrict to one top-level folder, e.g. decisions")
    args = ap.parse_args()
    if args.cmd == "index":
        index(args.vault)
    else:
        recall(args.vault, args.query, args.n, args.scope)


if __name__ == "__main__":
    main()
