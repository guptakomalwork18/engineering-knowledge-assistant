
from app.services.document_loader import load_document
from app.services.text_chunker import split_into_chunks


# Step 1: Load the PDF document
documents = load_document("docs/sample_kafka_notes.pdf")

# Step 2: Split the extracted text into chunks
chunks = split_into_chunks(
    documents,
    chunk_size=500,
    overlap=100,
)

# Step 3: Display the results
print(f"\nTotal chunks created: {len(chunks)}")

for chunk in chunks:
    print("\n" + "=" * 60)

    print("Chunk Text:")
    print(chunk["text"])

    print("\nMetadata:")
    print(chunk["metadata"])

    print("\nChunk Length:")
    print(len(chunk["text"]))
