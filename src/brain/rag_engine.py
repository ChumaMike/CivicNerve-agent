import os
import shutil
from typing import List
from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# --- CONSTANTS ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
DATA_PATH = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(PROJECT_ROOT, "src/data/vector_db")

# Real sentence-transformer embeddings (384-dim, runs locally, no API cost)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

# Module-level cache so we load FAISS once per process lifecycle
_vector_db_cache = None


def _get_vector_db():
    global _vector_db_cache
    if _vector_db_cache is None:
        _vector_db_cache = FAISS.load_local(
            DB_PATH, embeddings, allow_dangerous_deserialization=True
        )
    return _vector_db_cache


def _invalidate_cache():
    global _vector_db_cache
    _vector_db_cache = None


def build_knowledge_base():
    """
    Ingests PDFs using IBM Docling to preserve TABLE structures in Bylaws,
    then stores real embeddings in FAISS.
    """
    print("🔹 [Docling] Starting Intelligent Ingestion...")

    converter = DocumentConverter()
    all_splits = []

    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: Data folder not found at {DATA_PATH}")
        return

    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".pdf"):
            file_path = os.path.join(DATA_PATH, filename)
            print(f"   📄 Parsing with Docling: {filename}...")

            try:
                result = converter.convert(file_path)
                markdown_text = result.document.export_to_markdown()

                headers_to_split_on = [
                    ("#", "Header 1"),
                    ("##", "Header 2"),
                    ("###", "Header 3"),
                ]
                splitter = MarkdownHeaderTextSplitter(
                    headers_to_split_on=headers_to_split_on
                )
                splits = splitter.split_text(markdown_text)

                for split in splits:
                    split.metadata["source"] = filename

                all_splits.extend(splits)
                print(f"      ✅ Extracted {len(splits)} structured chunks.")

            except Exception as e:
                print(f"      ❌ Failed to parse {filename}: {e}")

    if all_splits:
        print(f"   💾 Saving {len(all_splits)} chunks to Vector DB with real embeddings...")
        vector_db = FAISS.from_documents(all_splits, embeddings)
        vector_db.save_local(DB_PATH)
        _invalidate_cache()  # Reset cache so next query loads fresh index
        print("✅ Knowledge Base Built with real sentence-transformer embeddings!")
    else:
        print("⚠️ No documents processed. Please add PDFs to the 'data' folder.")


def query_knowledge_base(query: str) -> List[str]:
    """Retrieves the most relevant legal clauses for a given issue."""
    if not os.path.exists(DB_PATH):
        return ["Error: Knowledge Base not found. Run 'python -m src.brain.rag_engine' first."]

    try:
        vector_db = _get_vector_db()
        results = vector_db.similarity_search(query, k=3)
        return [doc.page_content for doc in results]

    except Exception as e:
        _invalidate_cache()  # Reset on error so next call tries a fresh load
        return [f"RAG Error: {str(e)}"]


if __name__ == "__main__":
    build_knowledge_base()
