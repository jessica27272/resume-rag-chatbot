import streamlit as st
import os
from document_processor import DocumentProcessor
from vector_database import VectorDatabase
from llm_interface import LLMInterface

st.set_page_config(page_title="Resume RAG Chatbot", page_icon="💼", layout="wide")

if 'vector_db' not in st.session_state:
    st.session_state.vector_db = None
if 'llm' not in st.session_state:
    st.session_state.llm = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'documents_loaded' not in st.session_state:
    st.session_state.documents_loaded = False

with st.sidebar:
    st.title("📚 Document Manager")
    st.markdown("---")
    st.subheader("Step 1: Upload Documents")
    st.info("Place your resume and project documents in the `documents/` folder")
    uploaded_files = st.file_uploader("Or upload files here", type=['pdf', 'docx', 'txt'], accept_multiple_files=True)
    if uploaded_files:
        os.makedirs("documents", exist_ok=True)
        for uploaded_file in uploaded_files:
            file_path = os.path.join("documents", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded!")
    st.markdown("---")
    st.subheader("Step 2: Process Documents")
    if st.button("🔄 Load & Index Documents", type="primary"):
        with st.spinner("Processing documents..."):
            try:
                processor = DocumentProcessor(docs_folder="documents")
                docs = processor.process_all_documents()
                if not docs:
                    st.error("No documents found! Please upload some files first.")
                else:
                    st.write(f"Found {len(docs)} document(s)")
                    all_chunks = []
                    for doc in docs:
                        chunks = processor.chunk_text(doc['content'])
                        for chunk in chunks:
                            all_chunks.append({'content': chunk, 'filename': doc['filename'], 'source': doc['source']})
                    st.write(f"Created {len(all_chunks)} text chunks")
                    st.session_state.vector_db = VectorDatabase()
                    if st.session_state.vector_db.get_collection_count() > 0:
                        st.session_state.vector_db.reset_collection()
                    st.session_state.vector_db.add_documents(all_chunks)
                    st.session_state.llm = LLMInterface()
                    st.session_state.documents_loaded = True
                    st.success("✅ Documents indexed successfully!")
                    st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")
    if st.session_state.vector_db:
        st.markdown("---")
        st.subheader("📊 Database Stats")
        count = st.session_state.vector_db.get_collection_count()
        st.metric("Total Chunks", count)
    st.markdown("---")
    st.subheader("ℹ️ About")
    st.caption("This RAG chatbot helps recruiters learn about your resume and projects through natural conversation.")

st.title("💼 Resume RAG Chatbot")
st.markdown("Ask me anything about the candidate's experience, skills, and projects!")

if not st.session_state.documents_loaded:
    st.warning("⚠️ Please upload and process documents using the sidebar first!")
    st.info("""**Quick Start:**
1. Upload your resume and project documents in the sidebar
2. Click 'Load & Index Documents'
3. Start chatting!""")
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message:
                with st.expander("📄 View Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.caption(f"**Source {i}:** {source['metadata'].get('filename', 'unknown')}")
                        st.text(source['content'][:200] + "...")
    if prompt := st.chat_input("Ask about skills, projects, experience..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Searching knowledge base..."):
                relevant_docs = st.session_state.vector_db.search(prompt, n_results=3)
                response_placeholder = st.empty()
                full_response = ""
                for chunk in st.session_state.llm.chat_stream(prompt, relevant_docs):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
                with st.expander("📄 View Sources"):
                    for i, doc in enumerate(relevant_docs, 1):
                        st.caption(f"**Source {i}:** {doc['metadata'].get('filename', 'unknown')}")
                        st.text(doc['content'][:200] + "...")
        st.session_state.messages.append({"role": "assistant", "content": full_response, "sources": relevant_docs})

st.markdown("---")
st.caption("Powered by ChromaDB + Sentence Transformers + Ollama | 100% Free & Local")
