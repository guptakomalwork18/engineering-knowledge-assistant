
from app.services.embedding_service import generate_embedding
from app.database.vector_store import search_chunks
from app.services.gemini_service import generate_response


def retrieve_context(
    question: str,
    n_results: int = 3,
) -> dict:
    if not question.strip():
        raise ValueError("Question cannot be empty.")
    
    if n_results <= 0:
        raise ValueError("n_results must be greater than zero.")

    query_embedding = generate_embedding(
        question,
        task_type="RETRIEVAL_QUERY",
    )

    results = search_chunks(
        query_embedding=query_embedding,
        n_results=n_results,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    if not documents:
        return {
            "context": "",
            "sources": [],
        }

    context_parts = []
    sources = []

    for index, (document, metadata) in enumerate(
        zip(documents, metadatas),
        start=1,
    ):
        source = metadata.get("source", "Unknown source")
        page_number = metadata.get("page_number")
        source_reference = f"[Source {index}]"

        if page_number is not None:
            source_description = f"{source}, Page {page_number}"
        else:
            source_description = source

        context_parts.append(
            f"{source_reference} ({source_description}):\n{document}"
        )

        sources.append({
            "reference": source_reference,
            "source": source,
            "page_number": page_number,
            "chunk_index": metadata.get("chunk_index"),
            "distance": distances[index - 1],
        })

    return {
        "context": "\n\n".join(context_parts),
        "sources": sources,
    }


def build_prompt(question: str, context: str) -> str:
    prompt = f"""
You are an Engineering Knowledge Assistant.

Answer the user's question using ONLY the information
provided in the retrieved context below.

Instructions:
1. Do not invent facts or use outside knowledge.
2. If the context does not contain enough information,
   clearly say that the knowledge base does not contain
   sufficient information to answer the question.
3. Explain the answer clearly and accurately.
4. Cite the sources using their reference labels,
   for example [Source 1].
5. Do not create citations that are not present in the context.

Retrieved context:

{context}

User question:

{question}

Answer:
"""

    return prompt.strip()


def answer_question(question: str, n_results: int = 3) -> dict:
    retrieved_data = retrieve_context(
        question=question,
        n_results=n_results,
    )

    context = retrieved_data["context"]
    sources = retrieved_data["sources"]

    if not context:
        return {
            "answer": (
                "I couldn't find relevant information in the "
                "knowledge base to answer your question."
            ),
            "sources": [],
        }

    prompt = build_prompt(
        question=question,
        context=context,
    )

    answer = generate_response(prompt)

    return {
        "answer": answer,
        "sources": sources,
    }
