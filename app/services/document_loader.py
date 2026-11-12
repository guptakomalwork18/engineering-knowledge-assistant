
import re
from pathlib import Path

from pypdf import PdfReader


def load_document(file_path: str) -> list[dict]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    file_extension = path.suffix.lower()
    documents = []

    if file_extension == ".pdf":
        reader = PdfReader(str(path))

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            # Normalize excessive whitespace from PDF extraction.
            text = re.sub(r"\s+", " ", text).strip()

            if text:
                documents.append({
                    "text": text,
                    "metadata": {
                        "source": path.name,
                        "page_number": page_number,
                    },
                })

    elif file_extension in {".txt", ".md"}:
        text = path.read_text(encoding="utf-8").strip()

        if text:
            documents.append({
                "text": text,
                "metadata": {
                    "source": path.name,
                    "page_number": None,
                },
            })

    else:
        raise ValueError(
            f"Unsupported file format: {file_extension}. "
            "Supported formats are PDF, TXT, and Markdown."
        )

    if not documents:
        raise ValueError("No readable text found in the document.")

    return documents
