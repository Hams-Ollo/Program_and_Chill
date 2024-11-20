from typing import List, Dict, Any, Optional
import logging
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from .document_processor import DocumentProcessor

class ChatAgent:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model=model,
            openai_api_key=api_key
        )
        self.doc_processor = DocumentProcessor()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Custom prompt template for the chatbot
        self.qa_template = """
        You are a helpful AI assistant with access to a knowledge base of documents.
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know. DO NOT try to make up an answer.
        If the question is not related to the context, just respond based on your general knowledge.
        
        Context: {context}
        
        Chat History: {chat_history}
        
        Question: {question}
        
        Answer: """
        
        self.qa_prompt = PromptTemplate(
            template=self.qa_template,
            input_variables=["context", "chat_history", "question"]
        )
        
        # Initialize the conversation chain
        self.conversation = None
        self._initialize_chain()
    
    def _initialize_chain(self):
        """Initialize the conversation chain with the vector store."""
        try:
            vectorstore = self.doc_processor.query_documents("", k=1)  # Just to initialize
            self.conversation = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=vectorstore.as_retriever(),
                memory=self.memory,
                combine_docs_chain_kwargs={"prompt": self.qa_prompt}
            )
        except Exception as e:
            logging.warning(f"No documents loaded yet: {str(e)}")
            self.conversation = None
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """Process a user message and return a response."""
        try:
            # If we have documents loaded, use RAG
            if self.conversation:
                response = self.conversation({"question": message})
                return {
                    "response": response["answer"],
                    "source_documents": response.get("source_documents", [])
                }
            
            # Otherwise, just use the base LLM
            response = self.llm.predict(message)
            return {
                "response": response,
                "source_documents": []
            }
        except Exception as e:
            logging.error(f"Error processing message: {str(e)}")
            return {
                "response": "I apologize, but I encountered an error processing your message. Please try again.",
                "source_documents": []
            }
    
    def add_documents(self, documents: List[Any]):
        """Add new documents to the knowledge base."""
        try:
            vectorstore = self.doc_processor.process_documents(documents)
            self.conversation = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=vectorstore.as_retriever(),
                memory=self.memory,
                combine_docs_chain_kwargs={"prompt": self.qa_prompt}
            )
        except Exception as e:
            logging.error(f"Error adding documents: {str(e)}")
            raise
