from app.database.vector_store import collection

# Retrieve records from ChromaDB.
records = collection.get(
    include=["documents", "metadatas", "embeddings"]
)

print("Total records:", collection.count())

print("\nFirst two stored records:\n")

for index in range(min(2, len(records["ids"]))):
    print("Record ID:", records["ids"][index])
    print("Document text:", records["documents"][index])
    print("Metadata:", records["metadatas"][index])
    print("Embedding dimensions:", len(records["embeddings"][index]))
    print("-" * 60)