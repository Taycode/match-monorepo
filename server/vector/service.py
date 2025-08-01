from pinecone import Pinecone, ServerlessSpec
from django.conf import settings
import openai
from openai import OpenAI
from typing import Optional, List


class VectorManager(object):
    openai_client = None
    pinecone_client = None

    def __init__(self, index_name: str, create_index: bool = True):
        pc = self.build_pinecone_client()
        indexes = pc.list_indexes()
        if not any(index_name in index["name"] for index in indexes) and create_index:
            pc.create_index(index_name, dimension=1536,
                            metric="cosine", spec=ServerlessSpec(
                                cloud="aws",
                                region="us-east-1"
                            ))  # Adjust dimension based on your embedding model
        self.index = pc.Index(index_name)

    @staticmethod
    def build_openai_client():
        if VectorManager.openai_client is None:
            VectorManager.openai_client = OpenAI(
                api_key=settings.OPENAPI_API_KEY  # Ensure the setting name is correct
            )
        return VectorManager.openai_client

    @staticmethod
    def build_pinecone_client():
        if VectorManager.pinecone_client is None:
            VectorManager.pinecone_client = Pinecone(
                api_key=settings.PINECONE_API_KEY)
        return VectorManager.pinecone_client

    # Function to generate embeddings using OpenAI
    @staticmethod
    def generate_embedding(text: str) -> list:
        response = openai.embeddings.create(
            input=text,
            model="text-embedding-ada-002"  # Replace with the embedding model of your choice
        )
        return response.data[0].embedding

    # 1. Add Resumes to Pinecone
    def add_text_to_index(self, unique_id: str, text: str, metadata: dict):
        embedding = self.generate_embedding(text)
        self.index.upsert([(unique_id, embedding, metadata)])

    def clear_index(self):
        self.index.delete(delete_all=True)

    # 2. Search for Talents Based on Job Description
    def search(self, text: Optional[str] = None, top_k: int = 10, filter={}, vector: Optional[List] = None):
        if vector is None and text is None:
            raise ValueError(
                "Either 'text' or 'vector' must be provided for search.")
        if vector is not None and text is not None:
            raise ValueError(
                "Only one of 'text' or 'vector' should be provided for search.")
        if vector is None:
            # Generate embedding for the text if not provided
            query_embedding = self.generate_embedding(text)
        else:
            query_embedding = vector
        results = self.index.query(vector=query_embedding,
                                   top_k=top_k,
                                   include_metadata=True,
                                   filter=filter)
        return results
