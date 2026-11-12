from app.services.document_loader import load_document

#documents = load_document("docs/sample_kafka_notes.md")

documents = load_document("docs/sample_kafka_notes.pdf")

for document in documents:
    print("Extracted Text:")
    print(document["text"])

    print("\nMetadata:")
    print(document["metadata"])