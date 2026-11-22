
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed_documents" / "chunks.json"
OUTPUT_FILE = BASE_DIR / "processed_documents" / "embedded_chunks.json"

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings():

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    texts = [chunk["content"] for chunk in chunks]

    # Convert text into numerical vectors
    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):

        embedded_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "source": chunk["source"],
            "content": chunk["content"],
            "embedding": embedding.tolist()
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            embedded_chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nEmbedding generation completed!")
    print("Total chunks:", len(embedded_chunks))
    print("Embedding dimensions:", len(embedded_chunks[0]["embedding"]))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    generate_embeddings()
