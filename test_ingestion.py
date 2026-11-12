from app.services.ingestion_service import ingest_document


result = ingest_document("docs/sample_kafka_notes.pdf")

print("\nDocument ingestion completed!")
print("Document:", result["document"])
print("Pages or sections:", result["pages_or_sections"])
print("Chunks created:", result["chunks_created"])
print("Chunks stored:", result["chunks_stored"])