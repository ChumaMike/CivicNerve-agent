import os
import shutil
from typing import List
from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings

# --- CONSTANTS ---
# Path Fix: Ensure we always find the data folder relative to this script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
DATA_PATH = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(PROJECT_ROOT, "src/data/vector_db")

# Fake Embeddings for Demo Speed (Replace with IBM Watsonx / OpenAI later)
embeddings = FakeEmbeddings(size=768)

def build_knowledge_base():
    """
    PHASE 1 UPGRADE: IBM DOCLING INGESTION
    Reads PDFs using Docling to preserve TABLE structures in Bylaws.
    """
    print("🔹 [Docling] Starting Intelligent Ingestion...")
    
    # 1. Initialize IBM Docling Converter
    converter = DocumentConverter()
    
    all_splits = []
    
    # 2. Scan Data Folder
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: Data folder not found at {DATA_PATH}")
        return

    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".pdf"):
            file_path = os.path.join(DATA_PATH, filename)
            print(f"   📄 Parsing with Docling: {filename}...")
            
            try:
                # --- THE MAGIC: DOCLING CONVERSION ---
                # Converts complex PDF layout into structured Markdown
                result = converter.convert(file_path)
                markdown_text = result.document.export_to_markdown()
                
                # 3. Smart Splitting (Preserves Headers & Tables)
                # We split by headers so "Section 5: Fines" stays together
                headers_to_split_on = [
                    ("#", "Header 1"),
                    ("##", "Header 2"),
                    ("###", "Header 3"),
                ]
                splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
                splits = splitter.split_text(markdown_text)
                
                # Add source metadata so we know which Bylaw it came from
                for split in splits:
                    split.metadata["source"] = filename
                    
                all_splits.extend(splits)
                print(f"      ✅ Successfully extracted {len(splits)} structured chunks.")
                
            except Exception as e:
                print(f"      ❌ Failed to parse {filename}: {e}")

    # 4. Save to Vector Database (FAISS)
    if all_splits:
        print(f"   💾 Saving {len(all_splits)} chunks to Vector DB...")
        vector_db = FAISS.from_documents(all_splits, embeddings)
        vector_db.save_local(DB_PATH)
        print("✅ Knowledge Base Built with Docling Intelligence!")
    else:
        print("⚠️ No documents processed. Please add PDFs to the 'data' folder.")

def query_knowledge_base(query: str) -> List[str]:
    """
    Retrieves the most relevant legal clauses for a given issue.
    """
    # Defensive: Check if DB exists
    if not os.path.exists(DB_PATH):
        return ["Error: Knowledge Base not found. Run 'python -m src.brain.rag_engine' first."]
    
    try:
        # Load the DB
        vector_db = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
        
        # Search for top 3 matches
        results = vector_db.similarity_search(query, k=3)
        
        # Return clean text
        return [doc.page_content for doc in results]
        
    except Exception as e:
        return [f"RAG Error: {str(e)}"]

if __name__ == "__main__":
    # Run this directly to rebuild the DB
    build_knowledge_base()