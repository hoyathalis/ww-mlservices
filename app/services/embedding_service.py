import os
import uuid
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

from app.models.article import Article
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_REGION = os.getenv("PINECONE_REGION")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
# Initialize Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Pinecone
pinecone = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION)

# Name of the Pinecone index
INDEX_NAME = PINECONE_INDEX

#Check if the index already exists; if not, create it
try:
    if INDEX_NAME not in pinecone.list_indexes():
        # Dimension depends on the embedding model
        pinecone.create_index(name=INDEX_NAME, dimension=384 , metric='cosine', spec=spec)  # all-MiniLM-L6-v2 outputs 384-dimensional vectors
except Exception as e:
    pass

# Connect to the index
index = pinecone.Index(INDEX_NAME)

def create_embedding(text: str):
    """
    Generate an embedding for the given text using Sentence Transformers.
    """
    embedding = model.encode(text).tolist()  # Convert to list for serialization
    return embedding

def store_article_in_pinecone(article: Article):
    """
    Generate embedding for the article and store it in Pinecone along with metadata.
    """
    try:
        # Generate a unique ID for the article
        article.id = str(uuid.uuid4())
        
        # Combine article components to create content
        content = f"{article.title} | {article.description} | {' '.join(article.tags)}"
 
        try:
            # Create embedding
            embedding = create_embedding(content)
        except Exception as e:
            print(f"Error creating embedding for article ID {article.id}: {e}")
            raise RuntimeError(f"Failed to create embedding for article with ID {article.id}.") from e

        # Prepare metadata
        article_metadata = {
            'id': article.id,
            'title': article.title,
            'url': article.url,
            'description': article.description,
            'tags': ' '.join(article.tags),
            'posted_at': article.posted_at.strftime('%Y-%m-%d')  
                        }
        try:
            index.upsert(
                vectors=[{
                    "id": str(article.id), 
                    "values": embedding, 
                    "metadata": article_metadata
                        }
                    ])

        except Exception as e:
            print(f"Error upserting article ID {article.id} into Pinecone: {e}")
            raise RuntimeError(f"Failed to upsert article with ID {article.id} into Pinecone.") from e
    
    except Exception as e:
        # Print the error and raise a more descriptive exception
        print(f"Error in store_article_in_pinecone for article ID {article.id}: {e}")
        raise RuntimeError(f"Failed to store article with ID {article.id} in Pinecone.") from e