import streamlit as st

from utils.pdf_processor import (
    extract_text_from_pdf,
    save_uploaded_file
)

from utils.text_chunker import (
    chunk_text
)

from utils.embedding_generator import (
    generate_embeddings,
    generate_query_embedding
)

from utils.vector_store import (
    store_embeddings,
    retrieve_relevant_chunks
)

from utils.llm import (
    generate_answer
)
from utils.memory import get_chat_history
from utils.session_manager import (
    save_chat_history,
    load_chat_history,
    get_saved_sessions,
    delete_session
)
from utils.reranker import rerank_documents

# ------------------------------------------------
# Page Config
# ------------------------------------------------

st.set_page_config(
    page_title="AI-Powered Document Assistant",
    page_icon="📚",
    layout="wide"
)

# ------------------------------------------------
# Session State
# ------------------------------------------------
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_session" not in st.session_state:
    st.session_state.current_session = None

# ------------------------------------------------
# Title
# ------------------------------------------------

st.title("📚 AI-Powered Document Assistant")

st.write(
    "AI-Powered Document Assistant"
)

# ------------------------------------------------
# Sidebar
# ------------------------------------------------

with st.sidebar:

    st.header("About")

    st.write("""
    Upload one or multiple Document
    and ask questions from them.
    """)

    st.divider()

    st.header("Previous Sessions")
    sessions=get_saved_sessions()
    selected_session=(
        st.selectbox(
            "Resume Chat",
            ["None"]+sessions
        )
    )
    if selected_session != "None":
        if st.button("Delete Session"):
            delete_session(selected_session)
            st.success("Session deleted successfully!")
            st.rerun()


if (selected_session != "None" and st.session_state.current_session != selected_session):
        st.session_state.messages = (
            load_chat_history(
                selected_session
            )
        )

        st.session_state.current_session = (
            selected_session
        )

        st.session_state.pdf_processed = True


# ------------------------------------------------
# File Upload
# ------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload Research Papers",
    type=["pdf"],
    accept_multiple_files=True
)

# ------------------------------------------------
# Process PDFs
# ------------------------------------------------

if uploaded_files:

    st.subheader("Uploaded Files")

    for file in uploaded_files:
        st.write(f"📄 {file.name}")
    # ------------------------------------------------
    # Load Previous Session
    # ------------------------------------------------

    if st.button("Process PDFs"):
        session_name = uploaded_files[0].name
        
        st.session_state.current_session = (
            session_name
        )
        st.session_state.messages = []
        save_chat_history(
            session_name,
            []
        )
        try:

            all_pages = []

            for uploaded_file in uploaded_files:

                pdf_path = save_uploaded_file(
                    uploaded_file
                )

                pages = extract_text_from_pdf(
                    pdf_path,
                    uploaded_file.name
                )

                all_pages.extend(pages)

            chunks = chunk_text(
                all_pages,
                st.session_state.current_session
            )

            with st.spinner(
                    "Generating embeddings..."):

                embeddings = generate_embeddings(
                    chunks
                )

            with st.spinner(
                    "Saving to ChromaDB..."):

                store_embeddings(
                    chunks,
                    embeddings
                )

            st.session_state.pdf_processed = True

            st.success(
                "PDFs Processed Successfully!"
            )

            st.subheader(
                "Statistics"
            )

            st.write(
                "Total PDFs:",
                len(uploaded_files)
            )

            st.write(
                "Total Chunks:",
                len(chunks)
            )

        except Exception as e:

            st.error(str(e))

# ------------------------------------------------
# Chat Section
# ------------------------------------------------


if st.session_state.pdf_processed:

    st.divider()

    st.header("Chat with Research Papers")

    # Show old messages

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            # Show sources if present

            if "sources" in message:

                st.markdown("### Sources")

                for source in message["sources"]:
                    st.markdown(f"- {source}")

    # User input

    user_question = st.chat_input(
        "Ask a question..."
    )

    if user_question:

        # Save user question

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        # Show current user message

        with st.chat_message("user"):
            st.markdown(user_question)

        try:

            with st.spinner(
                    "Searching Documents..."):

                query_embedding = (
                    generate_query_embedding(
                        user_question
                    )
                )
                results = (
                    retrieve_relevant_chunks(
                        query=user_question,
                        query_embedding=query_embedding,
                        session_name=st.session_state.current_session,
                        top_k=10
                    )
                )


            documents = results["documents"]
            documents = rerank_documents(
                user_question,
                documents,
                top_k=5
            )
            metadata_map = results["metadata_map"]
            metadatas = []

            for doc in documents:

                if doc in metadata_map:
                    metadatas.append(
                        metadata_map[doc]
                    )
            if not documents:

                answer = (
                    "No relevant information found."
                )

                sources = []

            else:

                context = "\n\n".join(
                    documents
                )
                chat_history = get_chat_history(
                    st.session_state.messages
                )
                with st.spinner(
                        "Generating Answer..."):
                    answer = generate_answer(
                        context,
                        user_question,
                        chat_history
                    )

                # Prepare sources

                sources = []

                for metadata in metadatas:

                    file_name = metadata.get(
                        "file_name",
                        "Unknown File"
                    )

                    page_number = metadata.get(
                        "page_number",
                        "Unknown Page"
                    )

                    source = (
                        f"{file_name} - "
                        f"Page {page_number}"
                    )

                    if source not in sources:
                        sources.append(source)

            # Show assistant response

            with st.chat_message("assistant"):

                st.markdown(answer)

                if sources:

                    st.markdown("### Sources")

                    for source in sources:
                        st.markdown(f"- {source}")


            # Save assistant message
            # VERY IMPORTANT

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                }
            )
            save_chat_history(
                st.session_state.current_session,
                st.session_state.messages
            )

        except Exception as e:

            st.error(f"Error: {str(e)}")