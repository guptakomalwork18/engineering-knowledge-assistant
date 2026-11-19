# Standard library imports
import logging
import sys
from pathlib import Path

# Third-party imports
import streamlit as st

# Add the project root to Python's module search path.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.rag_service import answer_question
from app.services.gemini_service import GeminiServiceError
from app.services.knowledge_base_service import initialize_knowledge_base

# Configure application logging.
logging.basicConfig(level=logging.INFO)

# Configure the Streamlit application.
st.set_page_config(
    page_title="Engineering Knowledge Assistant",
    page_icon="📚",
    layout="wide",
)


# Cache the knowledge-base initialization result.
# This prevents unnecessary initialization on Streamlit reruns.
@st.cache_resource(show_spinner="Preparing the engineering knowledge base...")
def prepare_knowledge_base() -> dict:
    return initialize_knowledge_base()


# Application heading.
st.title("📚 Engineering Knowledge Assistant")

st.caption(
    "An AI-powered assistant that answers engineering questions "
    "using document retrieval and Generative AI."
)

st.divider()


# Initialize the knowledge base before accepting questions.
st.header("Knowledge Base Status")

try:
    knowledge_base_status = prepare_knowledge_base()

    st.success("Knowledge base is ready.")

    for document in knowledge_base_status["documents"]:
        st.markdown(f"- **{document['document']}** " f"({document['chunks']} chunks)")

except Exception:
    logging.exception("Knowledge-base initialization failed")

    st.error("The knowledge base could not be initialized. " "Please try again later.")

    st.stop()


st.divider()


# Display information about the available knowledge base.
st.header("Available Knowledge Base")

st.write(
    "This demo uses a curated collection of engineering documents. "
    "Ask questions about the information contained in these documents."
)

st.markdown("- `sample_kafka_notes.md`")
st.markdown("- `sample_kafka_notes.pdf`")

st.info("This is a read-only public demo. Document uploads are disabled.")

st.divider()


# Question and answer section.
st.header("Ask Engineering Questions")

st.write(
    "Ask a question about Apache Kafka and the assistant "
    "will retrieve relevant information from the knowledge base."
)

question = st.text_area(
    "Enter your engineering question:",
    placeholder=(
        "Example: How does Kafka distribute messages "
        "among consumers in a consumer group?"
    ),
    height=100,
    max_chars=1000,
)

if st.button("Ask Assistant", type="primary"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        try:
            with st.spinner("Searching documents and generating your answer..."):
                result = answer_question(
                    question=question.strip(),
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
                st.info(
                    "No relevant sources were found. " "Please try another question."
                )

        except GeminiServiceError as error:
            logging.exception("Gemini service error")

            st.warning(error.user_message)

            st.caption(f"Technical error category: {error.category}")

        except Exception:
            logging.exception("Unexpected application error")

            st.error(
                "An unexpected application error occurred. " "Please try again later."
            )


st.divider()

st.caption(
    "Engineering Knowledge Assistant | " "Powered by Gemini, ChromaDB and Streamlit"
)
