
import json
from pathlib import Path
import chromadb

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed_documents" / "embedded_chunks.json"
DB_PATH = BASE_DIR / "vector_store"

# Create a persistent ChromaDB client
client = chromadb.PersistentClient(path=str(DB_PATH))


def store_embeddings():

    # Load the newly generated embeddings
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not chunks:
        raise ValueError("No embedded chunks found.")

    # Prepare data for ChromaDB
    ids = [chunk["chunk_id"] for chunk in chunks]

    documents = [chunk["content"] for chunk in chunks]

    embeddings = [chunk["embedding"] for chunk in chunks]

    metadatas = [
        {"source": chunk["source"]}
        for chunk in chunks
    ]

    # Delete the old collection if it exists
    existing_collections = [
        collection.name for collection in client.list_collections()
    ]

    if "hr_documents" in existing_collections:

        client.delete_collection(name="hr_documents")

        print("Old collection deleted successfully!")

    # Create a fresh collection
    collection = client.create_collection(
        name="hr_documents"
    )

    # Insert the latest embeddings
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("\nEmbeddings stored successfully in ChromaDB!")
    print("Total records:", collection.count())

    if collection.count() != len(chunks):
        raise ValueError(
            "ChromaDB record count does not match chunk count."
        )


if __name__ == "__main__":
    store_embeddings()
