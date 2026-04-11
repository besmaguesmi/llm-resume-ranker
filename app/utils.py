"""Helper functions for loading PDFs and splitting long text into smaller chunks
(necessary because LLMs have context limits and vector search works better on smaller pieces).
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP

def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    return loader.load()

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_documents(docs)