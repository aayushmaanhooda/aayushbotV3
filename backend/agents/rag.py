from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.tools import tool
import os
from pathlib import Path

load_dotenv()

# Get the absolute path to the agents directory
AGENTS_DIR = Path(__file__).parent

# Initialize Pinecone
api = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
pc = Pinecone(api_key=api)
index = pc.Index(index_name)
vector_store = PineconeVectorStore(embedding=embeddings, index=index)


def clear_pinecone_index():
    """
    Clear all vectors from the Pinecone index.
    Call this before uploading new documents to start fresh.
    """
    try:
        # Get index stats to check if there are any vectors
        stats = index.describe_index_stats()
        total_vectors = stats.get("total_vector_count", 0)

        if total_vectors == 0:
            print("ℹ️  Pinecone index is already empty")
            return True

        # Delete all vectors from all namespaces
        namespaces = stats.get("namespaces", {})

        if namespaces:
            for namespace in namespaces.keys():
                index.delete(delete_all=True, namespace=namespace)
                print(f"🗑️  Cleared namespace: {namespace}")
        else:
            # If no namespaces, delete from default namespace
            index.delete(delete_all=True, namespace="")
            print("🗑️  Cleared default namespace")

        print(f"✅ Successfully cleared {total_vectors} vectors from Pinecone index")
        return True
    except Exception as e:
        print(f"❌ Error clearing Pinecone index: {str(e)}")
        raise e


# Note: Document loading is separated into a function
# Call upload_documents() only once to populate your index
def upload_documents(pdf_path=None):
    """
    Upload documents to Pinecone vector store.
    Call this function only once to populate your index.
    """
    if pdf_path is None:
        pdf_path = str(AGENTS_DIR / "ragProfile.pdf")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        add_start_index=True,
    )
    all_splits = text_splitter.split_documents(docs)
    document_ids = vector_store.add_documents(documents=all_splits)
    print(f"✅ Uploaded {len(document_ids)} document chunks to Pinecone")
    return document_ids


@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """
    Retrieve information about Aayushmaan's background, skills, experience,
    projects, and blogs from the knowledge base.
    Use this for personal/professional queries about Aayushmaan.
    """
    retrieved_docs = vector_store.similarity_search(query, k=5)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs
