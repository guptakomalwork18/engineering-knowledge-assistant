from app.services.document_loader import load_document
from app.services.text_chunker import split_into_chunks
from app.services.embedding_service import generate_embedding
from app.database.vector_store import store_chunks


def ingest_document(file_path: str) -> dict:
    """
    Load a document, split it into chunks, generate embeddings,
    and store everything in ChromaDB.
    """

    # Step 1: Extract text from the document.
    documents = load_document(file_path)

    # Step 2: Split the extracted text into smaller chunks.
    chunks = split_into_chunks(documents)

    # Step 3: Generate a Gemini embedding for each chunk.
    embeddings = [
        generate_embedding(chunk["text"])
        for chunk in chunks
    ]

    # Step 4: Store chunks, embeddings, and metadata.
    stored_ids = store_chunks(chunks, embeddings)

    return {
        "document": file_path,
        "pages_or_sections": len(documents),
        "chunks_created": len(chunks),
        "chunks_stored": len(stored_ids),
    }