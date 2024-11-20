from typing import List, Dict, Any
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredFileLoader,
)
import os

class DocumentProcessor:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
    def load_document(self, file_path: str) -> List[Any]:
        """Load and split a document based on its file type."""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.pdf':
                loader = PyPDFLoader(file_path)
            elif file_extension == '.txt':
                loader = TextLoader(file_path)
            elif file_extension in ['.doc', '.docx']:
                loader = Docx2txtLoader(file_path)
            else:
                loader = UnstructuredFileLoader(file_path)
            
            documents = loader.load()
            split_docs = self.text_splitter.split_documents(documents)
            return split_docs
        except Exception as e:
            logging.error(f"Error loading document {file_path}: {str(e)}")
            raise

    def process_documents(self, documents: List[Any]) -> Chroma:
        """Process documents and store them in the vector store."""
        try:
            vectordb = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            vectordb.persist()
            return vectordb
        except Exception as e:
            logging.error(f"Error processing documents: {str(e)}")
            raise

    def query_documents(self, query: str, k: int = 5) -> List[Dict]:
        """Query the vector store for relevant documents."""
        try:
            vectordb = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            results = vectordb.similarity_search_with_relevance_scores(query, k=k)
            return [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "relevance": score
                }
                for doc, score in results
            ]
        except Exception as e:
            logging.error(f"Error querying documents: {str(e)}")
            return []
