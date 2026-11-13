
from app.services.rag_service import answer_question


# Test 1: Empty question
try:
    answer_question("   ")
    raise AssertionError("Empty question should have failed.")

except ValueError as error:
    print("Empty question test passed:", error)


# Test 2: Invalid number of search results
try:
    answer_question(
        "Explain Kafka",
        n_results=0,
    )
    raise AssertionError("Invalid n_results should have failed.")

except ValueError as error:
    print("Invalid n_results test passed:", error)


print("\nAll validation tests passed!")
