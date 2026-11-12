import uuid

import chromadb


# Create a persistent ChromaDB client.
client = chromadb.PersistentClient(path="chroma_db")

# Create or reuse our document collection.
collection = client.get_or_create_collection(
    name="engineering_knowledge",
    embedding_function=None,
    metadata={"hnsw:space": "cosine"},
)



def store_chunks(chunks: list[dict], embeddings: list[list[float]]) -> list[str]:
    """
    Store document chunks, embeddings, and source metadata.

    Re-ingesting the same document updates existing records
    instead of creating duplicates.
    """

    if len(chunks) != len(embeddings):
        raise ValueError("Each chunk must have exactly one embedding.")

    if not chunks:
        return []

    # This function expects chunks from one document at a time.
    source = chunks[0]["metadata"]["source"]

    if any(chunk["metadata"]["source"] != source for chunk in chunks):
        raise ValueError("All chunks must belong to the same source document.")

    # Fetch existing records for this source before updating.
    existing_records = collection.get(
        where={"source": source},
    )

    existing_ids = set(existing_records["ids"])

    ids = [
        str(uuid.uuid5(
            uuid.NAMESPACE_URL,
            (
                f"{source}:"
                f"{chunk['metadata'].get('page_number')}:"
                f"{chunk['metadata']['chunk_index']}"
            ),
        ))
        for chunk in chunks
    ]

    documents = [chunk["text"] for chunk in chunks]

    metadatas = [
        {
            key: value
            for key, value in chunk["metadata"].items()
            if value is not None
        }
        for chunk in chunks
    ]

    # Insert new records or update records with matching IDs.
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    # Remove old chunks that no longer exist in the updated document.
    current_ids = set(ids)
    obsolete_ids = list(existing_ids - current_ids)

    if obsolete_ids:
        collection.delete(ids=obsolete_ids)

    return ids



def search_chunks(
    query_embedding: list[float],
    n_results: int = 3,
) -> dict:
    """
    Find the most relevant document chunks for a query embedding.
    """

    total_records = collection.count()

    if total_records == 0:
        return {"ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]}

    if n_results <= 0:
        raise ValueError("n_results must be greater than zero.")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, total_records),
        include=["documents", "metadatas", "distances"],
    )

    return results