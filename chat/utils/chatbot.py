# chat/utils/chatbot.py

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
# from langchain.chains.combine_documents import RetrievalQA



# 1️⃣ Build the vectorstore from PDF (one time per PDF)
def create_vectorstore(pdf_path, vectorstore_path="vectorstore"):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(vectorstore_path)
    print("✅ Vectorstore created and saved successfully!")


# 2️⃣ Ask a question using existing vectorstore
def ask_question(query, vectorstore_path="vectorstore"):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model="gpt-3.5-turbo")
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)
    result = qa_chain.run(query)
    return result


