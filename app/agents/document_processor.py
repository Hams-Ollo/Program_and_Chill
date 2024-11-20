from typing import List, Dict, Any
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredFileLoader,
)
import os
import tempfile

class DocumentProcessor:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        os.makedirs(self.persist_directory, exist_ok=True)
        
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
            logging.info(f"Loading document: {file_path}")
            
            if file_extension == '.pdf':
                loader = PyPDFLoader(file_path)
            elif file_extension == '.txt':
                loader = TextLoader(file_path)
            elif file_extension in ['.doc', '.docx']:
                # Use UnstructuredWordDocumentLoader for better Word document handling
                loader = UnstructuredWordDocumentLoader(
                    file_path,
                    mode="elements",
                    strategy="fast"
                )
            else:
                loader = UnstructuredFileLoader(file_path)
            
            documents = loader.load()
            logging.info(f"Successfully loaded document with {len(documents)} elements")
            
            # Add source metadata
            for doc in documents:
                doc.metadata["source"] = os.path.basename(file_path)
                doc.metadata["file_type"] = file_extension
            
            split_docs = self.text_splitter.split_documents(documents)
            logging.info(f"Split document into {len(split_docs)} chunks")
            
            return split_docs
            
        except Exception as e:
            logging.error(f"Error loading document {file_path}: {str(e)}", exc_info=True)
            raise

    def process_documents(self, documents: List[Any]) -> Chroma:
        """Process documents and store them in the vector store."""
        try:
            logging.info(f"Processing {len(documents)} documents")
            
            # Create a new vector store
            vectordb = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            vectordb.persist()
            
            logging.info("Successfully processed and stored documents")
            return vectordb
            
        except Exception as e:
            logging.error(f"Error processing documents: {str(e)}", exc_info=True)
            raise

    def query_documents(self, query: str, k: int = 5) -> List[Dict]:
        """Query the vector store for relevant documents."""
        try:
            if not os.path.exists(self.persist_directory):
                logging.warning("No documents have been processed yet")
                return []
                
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
            logging.error(f"Error querying documents: {str(e)}", exc_info=True)
            return []
