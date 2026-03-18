from chatbot_core import build_qa_chain

print("🔄 Loading PDF and building RAG pipeline...")
qa_chain = build_qa_chain("example.pdf")

print("🧠 PDF RAG Chatbot ready! Type 'exit' to quit.")

while True:
    query = input("\n❓ Question: ")
    if query.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break
    
    result = qa_chain.invoke({"input": query})
    answer = result["answer"]
    
    print("\n💬 Answer:", answer)
    print("\n🔍 Source snippet:", result["context"][0].page_content[:300] + "...")