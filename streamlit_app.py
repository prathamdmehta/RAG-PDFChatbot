import streamlit as st
import os
from dotenv import load_dotenv
from chatbot_core import build_qa_chain

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📄 PDF RAG Chatbot")
st.markdown("**Chat with your PDF documents using AI-powered search**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # PDF file uploader
    uploaded_file = st.file_uploader(
        "Choose a PDF file", 
        type="pdf",
        help="Upload your PDF to start chatting"
    )
    
    if uploaded_file:
        # Save uploaded file
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success("✅ PDF uploaded!")
        st.info(f"📊 File: **{uploaded_file.name}**")
    
    # Cache chain
    @st.cache_resource
    def load_chain(pdf_path):
        return build_qa_chain(pdf_path)
    
    # Load chain if PDF exists
    if uploaded_file or os.path.exists("example.pdf"):
        pdf_path = "temp.pdf" if uploaded_file else "example.pdf"
        qa_chain = load_chain(pdf_path)
        st.success("🚀 RAG Pipeline ready!")
    else:
        st.warning("⚠️ Please upload a PDF first")
        st.stop()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show source for assistant messages
        if message["role"] == "assistant" and "source" in message:
            with st.expander("📍 Source"):
                st.markdown(message["source"][:500] + "..." if len(message["source"]) > 500 else message["source"])

# Chat input
if prompt := st.chat_input("Ask anything about your PDF..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = qa_chain.invoke({"input": prompt})
            answer = result["answer"]
            source = result["context"][0].page_content if result["context"] else "No source found"
            
            st.markdown(answer)
            
            # Store source with answer
            st.session_state.messages[-1]["role"] = "assistant"
            st.session_state.messages[-1]["content"] = answer
            st.session_state.messages[-1]["source"] = source

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
    st.markdown("• Sentence Transformers")