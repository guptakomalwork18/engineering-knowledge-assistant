
from app.services.rag_service import retrieve_context

question = "How does Kafka distribute messages and handle parallel processing?"

print("Testing real RAG retrieval...")

result = retrieve_context(
    question=question,
    n_results=3,
)

print("\nRetrieved Context:")
print(result["context"])

print("\nRetrieved Sources:")

for source in result["sources"]:
    print(
        f"{source['reference']} | "
        f"File: {source['source']} | "
        f"Page: {source['page_number']} | "
        f"Chunk: {source['chunk_index']} | "
        f"Distance: {source['distance']:.4f}"
    )

assert result["context"], "No context was retrieved."
assert result["sources"], "No sources were retrieved."

print("\nAll real retrieval checks passed!")
