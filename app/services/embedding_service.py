import os
import uuid
import pinecone
from app.models.article import Article
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")

# Initialize Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

# Name of the Pinecone index
INDEX_NAME = os.getenv("PINECONE_INDEX")

# Check if the index already exists; if not, create it
if INDEX_NAME not in pinecone.list_indexes():
    # Dimension depends on the embedding model
    pinecone.create_index(name=INDEX_NAME, dimension=384)  # all-MiniLM-L6-v2 outputs 384-dimensional vectors

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
    article.id = str(uuid.uuid4())
    content = f"{article.title} | {article.description} | {' '.join(article.tags)}"
    # Create embedding
    embedding = create_embedding(content)

    # Prepare metadata
    metadata = {
        'id' : article.id,
        'title': article.title,
        'url': article.url,
        'description' : article.description,
        'tags' : article.tags,
        'posted_at':article.posted_at,
        'metadata' : article.metadata
    }

    # Upsert into Pinecone
    index.upsert([
        (str(article.id), embedding, metadata)
    ])
