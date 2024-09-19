from typing import List, Dict
from app.models.article import Article, Interaction
from sentence_transformers import SentenceTransformer
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os
import numpy as np


def initialize_pinecone():
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_REGION = os.getenv("PINECONE_REGION")
    PINECONE_CLOUD = os.getenv("PINECONE_CLOUD")
    PINECONE_INDEX = os.getenv("PINECONE_INDEX")
    pinecone = Pinecone(api_key=PINECONE_API_KEY)
    spec = ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION)
    index = pinecone.Index(PINECONE_INDEX)

    return index


def get_mean_embedding(liked_articles_ids: List[str], index) -> np.ndarray:
    liked_embeddings = []

    for article_id in liked_articles_ids:
        response = index.fetch(ids=[article_id])
        if response and response['vectors']:
            embedding = response['vectors'][article_id]['values']
            liked_embeddings.append(embedding)
        else:
            print(f"No embedding found for article ID: {article_id}")

    if liked_embeddings:
        mean_embedding = np.mean(liked_embeddings, axis=0)
    else:
        mean_embedding = np.zeros(384)  

    return mean_embedding


def get_cosine_similarity_matches(index, mean_embedding: np.ndarray, top_k: int = 20) -> List[Dict]:

    query_response = index.query(
        vector=mean_embedding,
        top_k=top_k,
        include_values=False,  
        include_metadata=True  
    )
    return query_response['matches']  


def convert_metadata_types(metadata: dict) -> dict:
   
    if metadata is None:
        return {}  

    if 'year' in metadata and isinstance(metadata['year'], float):
        metadata['year'] = str(int(metadata['year'])) 
    if 'tags' in metadata:
        tags = metadata['tags']
        if isinstance(tags, str):  
            metadata['tags'] = [tags]
        elif not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            metadata['tags'] = []  

    return metadata

def fetch_recommendations(interactions: List[Interaction]) -> List[Article]:
    liked_articles_ids = [interaction.article_id for interaction in interactions if interaction.like > 0]
    print(f"Liked article IDs: {liked_articles_ids}")

    index = initialize_pinecone()

    mean_embedding = get_mean_embedding(liked_articles_ids, index)

    matches = get_cosine_similarity_matches(index, mean_embedding)

    articles = []
    for match in matches:
        article_id = match['id']
        metadata = match.get('metadata', {})
        
        metadata = convert_metadata_types(metadata)
        
        article = Article(
            id=article_id,
            title=metadata.get("title", None),  
            description=metadata.get("description", None),  
            tags=metadata.get("tags", []),  
            url=metadata.get("url", None),
            posted_at=metadata.get("posted_at", None), 
        )
        articles.append(article)

    return articles
