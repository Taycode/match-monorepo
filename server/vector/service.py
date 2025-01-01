from pinecone import Pinecone, ServerlessSpec
from django.conf import settings
import openai

pc = Pinecone(api_key=settings.PINECONE_API_KEY)


class VectorManager(object):
    def __init__(self, index_name: str, create_index: bool = True):
        if index_name not in pc.list_indexes() and create_index:
            pc.create_index(index_name, dimension=1536,
                            metric="cosine", spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                ))  # Adjust dimension based on your embedding model
        self.index = pc.Index(index_name)

    # Function to generate embeddings using OpenAI
    @staticmethod
    def generate_embedding(text: str) -> list:
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"  # Replace with the embedding model of your choice
        )
        return response["data"][0]["embedding"]

    # 1. Add Resumes to Pinecone
    def add_text_to_index(self, unique_id: str, text: str, metadata: dict):
        embedding = self.generate_embedding(text)
        self.index.upsert([(unique_id, embedding, metadata)])

    # 2. Search for Talents Based on Job Description
    def search(self, text: str, top_k: int = 10):
        query_embedding = self.generate_embedding(text)
        results = self.index.query(query_embedding, top_k=top_k, include_metadata=True)
        return results
