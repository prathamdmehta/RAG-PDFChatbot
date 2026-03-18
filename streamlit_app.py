import streamlit as st
import os
from dotenv import load_dotenv
from chatbot_core import build_qa_chain

load_dotenv()

st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📄 PDF RAG Chatbot")
st.markdown("**Chat with your PDF documents using AI-powered search**")

# NO CACHE - Always fresh PDF analysis
def load_chain(pdf_path):
    return build_qa_chain(pdf_path)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file", 
        type="pdf",
        help="Upload your PDF to start chatting"
    )
    
    # Clear cache button
    if st.button("🔄 Clear Cache & Reload", use_container_width=True):
        st.cache_resource.clear()
        st.success("✅ Cache cleared! Upload new PDF.")
        st.rerun()
    
    pdf_path = None
    if uploaded_file:
        # Save uploaded file
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())
        pdf_path = "temp.pdf"
        st.success(f"✅ {uploaded_file.name} loaded!")
        st.info("💡 Click 'Clear Cache' if switching PDFs")
    elif os.path.exists("example.pdf"):
        pdf_path = "example.pdf"
        st.info("📄 Using example.pdf")
    
    if not pdf_path:
        st.warning("⚠️ Please upload a PDF first")
        st.stop()
    
    # ALWAYS FRESH - No caching
    with st.spinner("🔄 Building RAG pipeline..."):
        qa_chain = load_chain(pdf_path)
    st.success("🚀 Ready to chat with your PDF!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "source" in message:
            with st.expander("📍 Source"):
                st.markdown(message["source"][:500] + "...")

# Chat input
if prompt := st.chat_input("Ask anything about your PDF..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = qa_chain.invoke({"input": prompt})
            answer = result["answer"]
            source = result["context"][0].page_content if result["context"] else "No source"
            
            st.markdown(answer)
            st.session_state.messages[-1] = {
                "role": "assistant", 
                "content": answer, 
                "source": source
            }

# Sidebar controls
with st.sidebar:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Built with:**")
    st.markdown("• LangChain v1.2")
    st.markdown("• OpenAI GPT-4o-mini")
    st.markdown("• FAISS Vector Store")