import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

VECTOR_STORE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "vector_store"))
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

# Initialize ChromaDB Client
chroma_client = chromadb.PersistentClient(path=VECTOR_STORE_DIR)
# We will use "documents" collection to store our text chunks
collection = chroma_client.get_or_create_collection(name="documents")

# Initialize Embedding Model (local, CPU friendly)
# The PDR recommended sentence-transformers, specifically miniLM or similar.
# e5-small, all-MiniLM-L6-v2 are good options.
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> list[float]:
    """Generate dense vector embedding for a given text."""
    # sentence-transformers outputs numpy arrays, we convert to list for chromadb
    return embedding_model.encode(text).tolist()

def chunk_text(text: str, chunk_size=500, overlap=50) -> list[str]:
    """Simple text chunker, splits text into words."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def ingest_document(doc_id: str, text: str, metadata: dict = None):
    """Chunks a document, embeds the chunks, and stores them in ChromaDB."""
    chunks = chunk_text(text)
    
    if not chunks:
        return
        
    embeddings = embedding_model.encode(chunks).tolist()
    
    metadatas = [metadata or {"source": doc_id} for _ in chunks]
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

def search_similar_documents(query: str, top_k: int = 3) -> list[str]:
    """Searches for the `top_k` most similar document chunks to the query."""
    query_embedding = get_embedding(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    if results['documents'] and len(results['documents']) > 0:
        return results['documents'][0]
    return []
