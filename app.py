import asyncio
import nest_asyncio
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

# ---- Fix for Streamlit + async gRPC ----
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
nest_asyncio.apply()
# ----------------------------------------

# Step 1: Configurations
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv('GOOGLE_API_KEY'))
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY"))

# Step 2: Steamlit App
st.set_page_config(page_title="RAG with LangChain", page_icon=":)", layout="wide")
st.title("IntelliSearch-A-RAG-Powered-Knowledge-Assistant-using-LangChain-and-Gemini")
uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt",'docx'])

if uploaded_file:
    with st.spinner("Processing file... Please wait!"):
        # Save uploaded file locally
        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Load file (document loader)
        if uploaded_file.name.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            
        elif uploaded_file.name.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            loader = TextLoader(file_path)

        docs = loader.load()

        # Split text
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        # Embeddings + Vector store
        vectorstore = FAISS.from_documents(chunks, embeddings)
        retriever = vectorstore.as_retriever()

        # RAG chain
        qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

        st.success(" File processed successfully!")

        # Ask a question
        user_query = st.text_input("Ask a question from your file:")
        if st.button("Get Answer"):
            if user_query.strip() != "":
                with st.spinner("Fetching answer... 🤔"):
                    response = qa(user_query)
                    
                    # Show Answer
                    st.subheader("💡 Answer")
                    st.write(response["result"])

                    # Show Metadata (Sources)
                    st.subheader("📎 Sources / Metadata")
                    for i, doc in enumerate(response["source_documents"], 1):
                        st.markdown(f"**Source {i}:** {doc.metadata}")
                        st.write(doc.page_content[:200] + "...")
