import tempfile
import traceback
from pathlib import Path

import streamlit as st

from app.services.ingestion_service import ingest_document
from app.services.rag_service import answer_question
from app.services.gemini_service import GeminiServiceError

# Configure the Streamlit application.
st.set_page_config(
    page_title="Engineering Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
)


# Application heading.
st.title("Engineering Knowledge Assistant")

st.caption("Your AI-powered assistant for exploring " "engineering documentation.")

st.divider()


# Document upload section.
st.header("1. Upload Engineering Documents")

st.write(
    "Upload PDF, TXT, or Markdown documents "
    "to build your engineering knowledge base."
)

uploaded_file = st.file_uploader(
    "Choose an engineering document",
    type=["pdf", "txt", "md"],
)

if uploaded_file is not None:
    st.write(f"Selected file: **{uploaded_file.name}**")

    if st.button("Process Document"):
        try:
            with st.spinner("Processing document and generating embeddings..."):
                # Create a temporary directory.
                with tempfile.TemporaryDirectory() as temp_dir:

                    # Preserve the original filename.
                    safe_filename = Path(uploaded_file.name).name
                    file_path = Path(temp_dir) / safe_filename

                    # Save the uploaded file temporarily.
                    file_path.write_bytes(uploaded_file.getvalue())

                    # Pass the temporary file path to our backend.
                    result = ingest_document(str(file_path))

            st.success("Document processed successfully!")

            st.write(f"**Document:** {uploaded_file.name}")
            st.write(f"**Pages or sections:** " f"{result['pages_or_sections']}")
            st.write(f"**Chunks created:** {result['chunks_created']}")
            st.write(f"**Chunks stored:** {result['chunks_stored']}")

        except Exception as error:
            traceback.print_exc()
            st.error(f"Document processing failed: {error}")


st.divider()


# Question and answer section.
st.header("2. Ask Engineering Questions")

st.write("Ask questions based on the documents " "you have uploaded.")

question = st.text_area(
    "Enter your engineering question:",
    placeholder="Example: How does Kafka handle parallel processing?",
    height=100,
)

if st.button("Ask Assistant", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")

    else:
        try:
            with st.spinner("Searching documents and generating your answer..."):
                result = answer_question(
                    question=question,
                    n_results=3,
                )

            st.subheader("Answer")
            st.markdown(result["answer"])

            st.subheader("Sources")

            if result["sources"]:
                for source in result["sources"]:
                    page = source["page_number"]

                    if page is not None:
                        location = f"Page {page}"
                    else:
                        location = "Page information unavailable"

                    st.markdown(
                        f"- **{source['reference']}** — "
                        f"{source['source']} ({location})"
                    )
            else:
                st.info("No relevant sources were found.")

        except GeminiServiceError as error:
            traceback.print_exc()

            st.warning(error.user_message)

            st.caption(f"Technical error category: {error.category}")

        except Exception as error:
            traceback.print_exc()

            st.error(
                "An unexpected application error occurred. " "Please try again later."
            )
