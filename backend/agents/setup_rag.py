"""
One-time script to upload documents to Pinecone.
Run this only once to populate your vector store with the PDF content.
"""

from rag import upload_documents
import sys

if __name__ == "__main__":
    print("📄 Starting document upload to Pinecone...")
    print("⚠️  This should only be run once to populate your index.")

    try:
        pdf_path = "ragProfile.pdf"
        if len(sys.argv) > 1:
            pdf_path = sys.argv[1]

        document_ids = upload_documents(pdf_path)
        print(f"✅ Successfully uploaded {len(document_ids)} document chunks!")
        print("🎉 Your RAG system is ready to use!")

    except Exception as e:
        print(f"❌ Error uploading documents: {str(e)}")
        sys.exit(1)
