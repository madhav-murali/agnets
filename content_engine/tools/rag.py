import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class SimpleRAG:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        # Initialize with a temporary directory or persistent one if needed
        self.vectorstore = None

    def ingest_text(self, text, source="user_input"):
        """Ingests raw text into the vector store."""
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.create_documents([text], metadatas=[{"source": source}])
        
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(documents=splits, embedding=self.embeddings)
        else:
            self.vectorstore.add_documents(splits)

    def query(self, query):
        """Retrieves relevant documents."""
        if self.vectorstore is None:
            return "No documents uploaded."
        
        retriever = self.vectorstore.as_retriever()
        docs = retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in docs])
