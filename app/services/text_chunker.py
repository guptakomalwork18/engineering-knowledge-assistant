
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

            # Find a word boundary instead of cutting mid-word.
            if end < len(text):
                boundary = text.rfind(" ", start, end)

                if boundary <= start:
                    boundary = text.find(" ", end)

                if boundary != -1:
                    end = boundary

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

            if end >= len(text):
                break

            # Calculate the next starting position while retaining overlap.
            next_start = max(0, end - overlap)

            # Move the start to a word boundary.
            next_boundary = text.find(" ", next_start, end)

            if next_boundary != -1:
                next_start = next_boundary + 1

            # Safety check to guarantee forward progress.
            if next_start <= start:
                next_start = end

            start = next_start

    return chunks
