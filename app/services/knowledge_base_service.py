from pathlib import Path

from app.database.vector_store import count_chunks_for_source
from app.services.document_loader import load_document
from app.services.text_chunker import split_into_chunks
from app.services.ingestion_service import ingest_document

# Resolve the project root independently of the terminal's
# current working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Documents included in the public demo.
SAMPLE_DOCUMENTS = [
    "sample_kafka_notes.md",
    "sample_kafka_notes.pdf",
]


def initialize_knowledge_base() -> dict:
    """
    Ensure all configured sample documents are available
    in the ChromaDB knowledge base.
    """

    results = []

    for filename in SAMPLE_DOCUMENTS:

        # Build the absolute path to the sample document.
        file_path = PROJECT_ROOT / "docs" / filename

        if not file_path.is_file():
            raise FileNotFoundError(f"Knowledge-base document not found: {file_path}")

        # Calculate how many chunks the document should produce.
        documents = load_document(str(file_path))
        expected_chunks = len(split_into_chunks(documents))

        # Check how many chunks are already stored.
        existing_chunks = count_chunks_for_source(filename)

        if existing_chunks == expected_chunks and expected_chunks > 0:
            results.append(
                {
                    "document": filename,
                    "status": "already_available",
                    "chunks": existing_chunks,
                }
            )

        else:
            # Ingest missing or incomplete documents.
            ingestion_result = ingest_document(str(file_path))

            results.append(
                {
                    "document": filename,
                    "status": "ingested",
                    "chunks": ingestion_result["chunks_stored"],
                }
            )

    return {
        "status": "ready",
        "documents": results,
    }
