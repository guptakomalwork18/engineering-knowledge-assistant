
def split_into_chunks(
    documents: list[dict],
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[dict]:
    """
    Split extracted documents into smaller text chunks.

    Each chunk retains the original document metadata
    and receives its own chunk index.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    chunks = []

    for document in documents:
        text = document["text"]
        metadata = document["metadata"]

        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        **metadata,
                        "chunk_index": chunk_index,
                    },
                })

                chunk_index += 1

            # Stop when we have reached the end of the document.
            if end == len(text):
                break

            # Move forward while retaining the configured overlap.
            start = end - overlap

    return chunks
