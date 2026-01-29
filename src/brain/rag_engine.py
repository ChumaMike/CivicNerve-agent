import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_PATH = "data/"
DB_PATH = "vector_db"

def build_knowledge_base():
    """Reads Real PDFs AND Text files to build the Brain"""
    print("🧠 Reading Knowledge Base (PDFs + Text)...")
    
    documents = []
    
    # 1. Load PDF Files (The Real Laws)
    # This automatically finds all .pdf files in data/
    if any(f.endswith(".pdf") for f in os.listdir(DATA_PATH)):
        print("   -> Found PDF documents. Loading...")
        pdf_loader = PyPDFDirectoryLoader(DATA_PATH)
        documents.extend(pdf_loader.load())

    # 2. Load Text Files (Your Notes)
    # This finds all .txt files
    if any(f.endswith(".txt") for f in os.listdir(DATA_PATH)):
        print("   -> Found Text notes. Loading...")
        text_loader = DirectoryLoader(DATA_PATH, glob="**/*.txt", loader_cls=TextLoader)
        documents.extend(text_loader.load())
    
    if not documents:
        print("❌ CRITICAL: No files found in 'data/'! Please add a PDF or .txt file.")
        return

    print(f"   -> Processing {len(documents)} pages of knowledge...")

    # 3. Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    
    # 4. Create Embeddings
    print("   -> Converting text to AI Vectors (this takes a moment)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # 5. Build & Save Database
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_PATH)
    print("✅ Knowledge Base Built! Saved to 'vector_db'")

def query_knowledge_base(query):
    """Searches the Laws for the answer"""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Load the DB with dangerous deserialization allowed (Safe since we built it)
    try:
        db = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
    except Exception:
        return ["Error: Knowledge Base not found. Run src/rag_engine.py first."]
    
    # Search for top 2 matching laws
    docs = db.similarity_search(query, k=2)
    return [doc.page_content for doc in docs]

if __name__ == "__main__":
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
    build_knowledge_base()