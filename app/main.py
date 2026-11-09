from app.services.gemini_service import generate_response


def main():
    prompt = "Explain Retrieval-Augmented Generation (RAG) in simple terms."

    response = generate_response(prompt)

    print("\nGemini Response:\n")
    print(response)


if __name__ == "__main__":
    main()