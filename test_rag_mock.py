
from unittest.mock import patch

from app.services.rag_service import answer_question


mock_embedding = [0.1, 0.2, 0.3]

mock_search_results = {
    "documents": [[
        "Kafka distributes partitions across consumers."
    ]],
    "metadatas": [[
        {
            "source": "sample_kafka_notes.pdf",
            "page_number": 2,
            "chunk_index": 0,
        }
    ]],
    "distances": [[0.15]],
}

mock_answer = (
    "Kafka distributes partitions across consumers "
    "within a consumer group. [Source 1]"
)

with patch(
    "app.services.rag_service.generate_embedding",
    return_value=mock_embedding,
) as embedding_mock:

    with patch(
        "app.services.rag_service.search_chunks",
        return_value=mock_search_results,
    ) as search_mock:

        with patch(
            "app.services.rag_service.generate_response",
            return_value=mock_answer,
        ) as generation_mock:

            result = answer_question(
                "How does Kafka distribute messages?"
            )

            print("Generated Answer:")
            print(result["answer"])

            print("\nRetrieved Sources:")
            print(result["sources"])

            assert result["answer"] == mock_answer
            assert len(result["sources"]) == 1
            assert result["sources"][0]["reference"] == "[Source 1]"

            embedding_mock.assert_called_once()
            search_mock.assert_called_once()
            generation_mock.assert_called_once()

            print("\nAll mocked RAG tests passed!")
