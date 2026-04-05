import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# Path where vector DB will be stored
DB_PATH = "faiss_index"

# Load embedding model (used to convert text → vectors)
embedding = HuggingFaceEmbeddings()


#  STORE FUNCTION
def store_in_vector_db(text: str):
    """
    Stores the generated report into vector database.
    """

    # Convert text into Document format
    doc = Document(page_content=text)

    try:
        # If DB already exists → load and append
        if os.path.exists(DB_PATH):
            db = FAISS.load_local(DB_PATH, embedding)
            db.add_documents([doc])
        else:
            # Create new DB
            db = FAISS.from_documents([doc], embedding)

        # Save DB locally
        db.save_local(DB_PATH)

        print(" Data stored in Vector DB")

    except Exception as e:
        print(f" Error storing data: {e}")


# SEARCH FUNCTION (RAG)
def search_vector_db(query: str) -> str:
    """
    Searches previous reports from vector database.
    Returns relevant content or empty string if not found.
    """

    try:
        # If DB doesn't exist → no previous data
        if not os.path.exists(DB_PATH):
            print(" No Vector DB found")
            return ""

        # Load DB
        db = FAISS.load_local(DB_PATH, embedding)

        # Search similar content
        results = db.similarity_search(query, k=3)

        if not results:
            print(" No relevant data found in RAG")
            return ""

        print(" RAG SEARCH USED")

        # Combine results into text
        combined_text = "\n\n".join([doc.page_content for doc in results])

        return combined_text

    except Exception as e:
        print(f"Error in RAG search: {e}")
        return ""