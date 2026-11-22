
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "vector_store"

# Load the same embedding model used earlier
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to the existing ChromaDB database
client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_collection(
    name="hr_documents"
)


def retrieve_documents(question, top_k=5):

    # Convert the user's question into an embedding
    question_embedding = model.encode(question).tolist()

    # Search ChromaDB for similar chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, collection.count())
    )

    retrieved_chunks = []

    for i in range(len(results["documents"][0])):

        retrieved_chunks.append({
            "content": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })

    return retrieved_chunks


if __name__ == "__main__":

    question = input("Enter your HR question: ")

    results = retrieve_documents(question)

    print("\nRETRIEVED HR INFORMATION\n")

    for index, result in enumerate(results, start=1):

        print(f"\nResult {index}")
        print("Source:", result["source"])
        print("Distance:", result["distance"])
        print("Content:")
        print(result["content"])
        print("-" * 60)
