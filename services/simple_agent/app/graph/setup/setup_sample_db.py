from langchain_community.vectorstores import Qdrant
from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

qdrant = QdrantClient(
    host=os.environ.get("QDRANT_HOST"),
    port=int(os.environ.get("QDRANT_PORT"))
)

qdrant.recreate_collection(
    collection_name="SCKS",
    vectors_config=models.VectorParams(
        size=960,  # adjust based on your model
        distance=models.Distance.COSINE
    )
)

embeddings = OllamaEmbeddings(
        model=os.environ.get("OLLAMA_MODEL"),
        base_url=os.environ.get("OLLAMA_BASE_URL"), 
    )

# Example: create a vector store
vector_store = QdrantVectorStore(
    client=qdrant,
    collection_name="SCKS",
    embedding=embeddings,
)

docs_list = UnstructuredExcelLoader("graph/setup/SCKS.xlsx", mode="elements").load()

vector_store.add_documents(docs_list)