import chromadb
from chromadb.config import Settings
import json
from typing import Dict, List, Optional, Union
import logging

class DatabaseManager:
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize the database manager with ChromaDB."""
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.content_collection = self.client.get_or_create_collection(
            name="content_plans",
            metadata={"hnsw:space": "cosine"}
        )
        self.social_collection = self.client.get_or_create_collection(
            name="social_posts",
            metadata={"hnsw:space": "cosine"}
        )
        logging.info("Database manager initialized with ChromaDB")

    def add_content_plan(self, plan_id: str, content: Dict, embeddings: Optional[List[float]] = None) -> None:
        """Add a content plan to the database."""
        try:
            self.content_collection.add(
                documents=[json.dumps(content)],
                metadatas=[{"type": "content_plan"}],
                ids=[plan_id]
            )
            logging.info(f"Added content plan with ID: {plan_id}")
        except Exception as e:
            logging.error(f"Error adding content plan: {str(e)}")
            raise

    def add_social_post(self, post_id: str, post_data: Dict, embeddings: Optional[List[float]] = None) -> None:
        """Add a social media post to the database."""
        try:
            self.social_collection.add(
                documents=[json.dumps(post_data)],
                metadatas=[{"type": "social_post"}],
                ids=[post_id]
            )
            logging.info(f"Added social post with ID: {post_id}")
        except Exception as e:
            logging.error(f"Error adding social post: {str(e)}")
            raise

    def get_content_plan(self, plan_id: str) -> Optional[Dict]:
        """Retrieve a content plan by ID."""
        try:
            result = self.content_collection.get(ids=[plan_id])
            if result and result['documents']:
                return json.loads(result['documents'][0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving content plan: {str(e)}")
            return None

    def get_social_post(self, post_id: str) -> Optional[Dict]:
        """Retrieve a social media post by ID."""
        try:
            result = self.social_collection.get(ids=[post_id])
            if result and result['documents']:
                return json.loads(result['documents'][0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving social post: {str(e)}")
            return None

    def query_content_plans(self, query_text: str, n_results: int = 5) -> List[Dict]:
        """Query content plans using text similarity."""
        try:
            results = self.content_collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return [json.loads(doc) for doc in results['documents'][0]]
        except Exception as e:
            logging.error(f"Error querying content plans: {str(e)}")
            return []

    def query_social_posts(self, query_text: str, n_results: int = 5) -> List[Dict]:
        """Query social media posts using text similarity."""
        try:
            results = self.social_collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return [json.loads(doc) for doc in results['documents'][0]]
        except Exception as e:
            logging.error(f"Error querying social posts: {str(e)}")
            return []

    def update_content_plan(self, plan_id: str, content: Dict) -> bool:
        """Update an existing content plan."""
        try:
            self.content_collection.update(
                documents=[json.dumps(content)],
                ids=[plan_id]
            )
            logging.info(f"Updated content plan with ID: {plan_id}")
            return True
        except Exception as e:
            logging.error(f"Error updating content plan: {str(e)}")
            return False

    def update_social_post(self, post_id: str, post_data: Dict) -> bool:
        """Update an existing social media post."""
        try:
            self.social_collection.update(
                documents=[json.dumps(post_data)],
                ids=[post_id]
            )
            logging.info(f"Updated social post with ID: {post_id}")
            return True
        except Exception as e:
            logging.error(f"Error updating social post: {str(e)}")
            return False

    def delete_content_plan(self, plan_id: str) -> bool:
        """Delete a content plan by ID."""
        try:
            self.content_collection.delete(ids=[plan_id])
            logging.info(f"Deleted content plan with ID: {plan_id}")
            return True
        except Exception as e:
            logging.error(f"Error deleting content plan: {str(e)}")
            return False

    def delete_social_post(self, post_id: str) -> bool:
        """Delete a social media post by ID."""
        try:
            self.social_collection.delete(ids=[post_id])
            logging.info(f"Deleted social post with ID: {post_id}")
            return True
        except Exception as e:
            logging.error(f"Error deleting social post: {str(e)}")
            return False
