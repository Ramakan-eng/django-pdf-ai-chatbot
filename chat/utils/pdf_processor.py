from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os

def create_vectorstore(pdf_path, store_path="vectorstore"):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)

    vectorstore.save_local(store_path)
    print(f"✅ Vectorstore saved at: {store_path}")

