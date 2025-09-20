# milvus_ingest.py
import os
import re
import json
import uuid
from typing import List
from sentence_transformers import SentenceTransformer
from pymilvus import (
    connections, FieldSchema, CollectionSchema, DataType,
    Collection, utility
)

CLEANED_DIR = "cleaned_docs"
COLLECTION_NAME = "cloudstack_docs"
DIMENSION = 1024  # BGE-M3 embedding size

# -----------------------------
# Milvus connection
# -----------------------------
connections.connect("default", host="localhost", port="19530")

# -----------------------------
# Embedding model
# -----------------------------
print("🔄 Loading embedding model (BAAI/bge-m3)...")
model = SentenceTransformer("BAAI/bge-m3")
print("✅ Model loaded.")

# -----------------------------
# Collection schema
# -----------------------------
def ensure_collection():
    if utility.has_collection(COLLECTION_NAME):
        return Collection(COLLECTION_NAME)

    print("📁 Creating Milvus collection with metadata fields...")
    fields = [
        FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=36),
        FieldSchema(name="resource", dtype=DataType.VARCHAR, max_length=128),
        FieldSchema(name="required_fields", dtype=DataType.VARCHAR, max_length=2048),  # JSON string
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=DIMENSION),
    ]
    schema = CollectionSchema(fields, description="CloudStack Terraform Docs + schema metadata")
    col = Collection(name=COLLECTION_NAME, schema=schema)
    col.create_index(
        field_name="embedding",
        index_params={"metric_type": "COSINE", "index_type": "IVF_FLAT", "params": {"nlist": 128}},
    )
    print("✅ Collection created and indexed.")
    return col

collection = ensure_collection()

# -----------------------------
# Helpers
# -----------------------------
def extract_resource_name(filename: str) -> str | None:
    """
    Example filename:
      registry.terraform.io_providers_cloudstack_cloudstack_latest_docs_resources_instance.md
    -> cloudstack_instance
    """
    m = re.search(r"resources_([^.]+)\.md$", filename)
    return f"cloudstack_{m.group(1)}" if m else None

def slice_argument_reference_section(text: str) -> str:
    """
    Grab only the 'Argument Reference' section to avoid false positives.
    Handles headings like:
      ## Argument Reference
      ## [Argument Reference](#argument-reference)
    Stops at next '## ' heading (Attributes/Import/etc.).
    """
    start = re.search(r"^##\s*(?:\[[^\]]*Argument Reference[^\]]*\]\([^)]+\)|Argument Reference)\s*$",
                      text, flags=re.IGNORECASE | re.MULTILINE)
    if not start:
        return text  # fallback: whole text

    section = text[start.end():]
    end = re.search(r"^\s*##\s+", section, flags=re.MULTILINE)  # next H2
    return section[:end.start()] if end else section

def extract_required_fields(text: str) -> List[str]:
    """
    Match these forms inside the Argument Reference section:
      - [`name`](...link...) - (Required)
      - `name` - (Required)
      - name - (Required)
    Allow for escaped dash '\-' or plain '-'.
    """
    section = slice_argument_reference_section(text)
    fields = set()

    dash = r"\s*(?:-|\\-)\s*"  # matches '-' or '\-' with optional spaces

    patterns = [
        # - [`name`](...) - (Required)
        rf"^\s*-\s*\[\s*`?([a-zA-Z0-9_]+)`?\s*\]\([^)]+\){dash}\(Required\)",
        # - `name` - (Required)
        rf"^\s*-\s*`([a-zA-Z0-9_]+)`{dash}\(Required\)",
        # - name - (Required)
        rf"^\s*-\s*([a-zA-Z0-9_]+){dash}\(Required\)",
    ]

    for pat in patterns:
        for m in re.finditer(pat, section, flags=re.MULTILINE):
            fields.add(m.group(1))

    return sorted(fields)

def split_text(text: str, max_words: int = 300) -> List[str]:
    chunks, cur, words = [], [], 0
    for line in text.splitlines():
        w = len(line.split())
        if words + w > max_words and cur:
            chunks.append("\n".join(cur))
            cur, words = [], 0
        cur.append(line)
        words += w
    if cur:
        chunks.append("\n".join(cur))
    return chunks

# -----------------------------
# Main ingestion
# -----------------------------
def process_documents():
    total_files = 0
    total_chunks = 0

    for filename in os.listdir(CLEANED_DIR):
        if not filename.endswith(".md"):
            continue

        resource_name = extract_resource_name(filename)
        if not resource_name:
            print(f"↪️  Skipping (not a resource doc): {filename}")
            continue

        path = os.path.join(CLEANED_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        required = extract_required_fields(raw_text)
        chunks = split_text(raw_text)

        # Debug: show what we found
        print(f"📄 {filename} → resource={resource_name}")
        if required:
            print(f"   🔖 Required fields: {required}")
        else:
            print("   ⚠️  No required fields detected in Argument Reference.")

        required_json = json.dumps(required, ensure_ascii=False)

        # Insert all chunks with the same metadata
        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk:
                continue
            emb = model.encode(chunk).tolist()
            doc_id = str(uuid.uuid4())
            collection.insert([
                [doc_id],
                [resource_name],
                [required_json],
                [chunk],
                [emb],
            ])
            total_chunks += 1

        total_files += 1
        print(f"   ✅ Stored {len(chunks)} chunks.")

    collection.flush()
    print(f"\n🚀 Ingestion complete. Files: {total_files}, Chunks: {total_chunks}")

if __name__ == "__main__":
    process_documents()
