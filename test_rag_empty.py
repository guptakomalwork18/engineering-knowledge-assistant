
from unittest.mock import patch

from app.services.rag_service import answer_question

with patch(
    "app.services.rag_service.generate_embedding",
    return_value=[0.1, 0.2, 0.3],
):

    with patch(
        "app.services.rag_service.search_chunks",
        return_value={
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
        },
    ):

        with patch(
            "app.services.rag_service.generate_response",
        ) as generation_mock:

            result = answer_question(
                "Explain Kafka consumer groups."
            )

            print("Generated Answer:")
            print(result["answer"])

            print("\nSources:")
            print(result["sources"])

            assert len(result["sources"]) == 0
            assert "couldn't find relevant information" in result["answer"]

            generation_mock.assert_not_called()

            print("\nAll empty retrieval checks passed!")

