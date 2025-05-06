from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_ollama import OllamaEmbeddings
import os

qdrant = QdrantClient(
    host=os.environ.get("QDRANT_HOST"),
    port=int(os.environ.get("QDRANT_PORT"))
)

embeddings = OllamaEmbeddings(
        model="smollm2",
        base_url=os.environ.get("OLLAMA_BASE_URL"), 
    )

vector_store = QdrantVectorStore(
    client=qdrant,
    collection_name="SCKS",
    embedding=embeddings,
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}  # Number of results to return
)