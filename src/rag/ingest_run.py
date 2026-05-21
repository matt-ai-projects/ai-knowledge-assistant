import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.rag.ingest import ingest_document

if __name__ == "__main__":
    ingest_document("docs/sample.txt")