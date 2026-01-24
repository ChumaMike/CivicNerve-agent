import json
from pathlib import Path
from docling.document_converter import DocumentConverter

class BlueprintParser:
    def __init__(self):
        self.converter = DocumentConverter()

    def parse_blueprint(self, file_path: str) -> str:
        """
        Ingests a PDF/Image blueprint and returns a structured Markdown string.
        """
        print(f"📄 [Docling] Ingesting blueprint: {file_path}...")
        
        try:
            # 1. Convert the document
            result = self.converter.convert(file_path)
            
            # 2. Export to Markdown (best format for LLMs)
            markdown_output = result.document.export_to_markdown()
            
            # 3. (Optional) In a real app, we would chunk this for VectorDB here
            return markdown_output
            
        except Exception as e:
            print(f"❌ [Docling] Error parsing file: {e}")
            return ""

# Quick test block
if __name__ == "__main__":
    parser = BlueprintParser()
    # Ensure you have a dummy PDF in data/blueprints to test!
    # print(parser.parse_blueprint("data/blueprints/sample_pipe.pdf"))