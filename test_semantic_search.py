from app.services.embedding_service import generate_embedding
from app.database.vector_store import search_chunks


question = "How does Kafka distribute messages and handle parallel processing?"

# Convert the user's question into an embedding.
query_embedding = generate_embedding(
    question,
    task_type="RETRIEVAL_QUERY",
)

# Search ChromaDB for the three most relevant chunks.
results = search_chunks(
    query_embedding=query_embedding,
    n_results=3,
)

print("\nUser question:", question)
print("\nRelevant document chunks:\n")

for index, document in enumerate(results["documents"][0]):
    print(f"Result {index + 1}:")
    print("Document:", document)
    print("Metadata:", results["metadatas"][0][index])
    print("Cosine distance:", results["distances"][0][index])
    print("-" * 60)