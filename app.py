import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.rag.chain import get_rag_chain
from src.rag.retriever import retrieve_chunks
from src.rag.ingest import ingest_document
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

with st.sidebar:
    st.title("🤖 AI Knowledge Assistant")
    st.caption("Powered by OpenAI + ChromaDB + LangChain")
    st.divider()

    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["txt", "pdf"],
        help="Supported formats: TXT, PDF"
    )

    if uploaded_file is not None:
        save_path = os.path.join("docs", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("📥 Ingest Document", type="primary"):
            with st.spinner("Reading and indexing your document..."):
                try:
                    ingest_document(save_path)
                    st.success(f"✅ {uploaded_file.name} indexed successfully!")
                    st.info("You can now ask questions below.")
                except Exception as e:
                    st.error(f"Ingestion failed: {str(e)}")

    st.divider()
    st.markdown("**How it works:**")
    st.markdown("1. 📄 Upload a document")
    st.markdown("2. 📥 Click Ingest Document")
    st.markdown("3. 💬 Ask questions in the chat")
    st.divider()
    st.markdown("**Example questions:**")
    st.markdown("- What are the user roles?")
    st.markdown("- How much does the Pro plan cost?")
    st.markdown("- How do I connect Slack?")

st.title("💬 Chat with your Documents")
st.caption("Ask anything about your uploaded documents.")

if st.button("🗑️ Clear chat"):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("📚 Source passages used"):
                for i, source in enumerate(message["sources"]):
                    st.markdown(f"**Passage {i+1}:**")
                    st.info(source)

if prompt := st.chat_input("Ask a question about your documents..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            try:
                chunks = retrieve_chunks(prompt)
                source_texts = [chunk.page_content for chunk in chunks]
                chain = get_rag_chain()
                answer = chain.invoke(prompt)
                st.markdown(answer)
                with st.expander("📚 Source passages used"):
                    for i, source in enumerate(source_texts):
                        st.markdown(f"**Passage {i+1}:**")
                        st.info(source)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": source_texts
                })
            except Exception as e:
                error_msg = str(e)
                if "no such table" in error_msg or "does not exist" in error_msg:
                    st.warning("⚠️ No documents ingested yet. Please upload and ingest a document first.")
                else:
                    st.error(f"Something went wrong: {error_msg}")