"""
Handles the entire pipeline of converting resumes into a searchable vector index using FAISS.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from app.config import EMBEDDING_MODEL, VECTOR_STORE_PATH
from app.utils import load_pdf, chunk_documents


class ResumeProcessor:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vector_store = None

    def process_resumes(self, resume_paths):
        all_chunks = []
        for path in resume_paths:
            docs = load_pdf(path)
            chunks = chunk_documents(docs)
            for c in chunks:
                c.metadata["source"] = path
            all_chunks.extend(chunks)
        self.vector_store = FAISS.from_documents(all_chunks, self.embeddings)
        self.vector_store.save_local(VECTOR_STORE_PATH)
        return len(all_chunks)

    def load_index(self):
        self.vector_store = FAISS.load_local(
            VECTOR_STORE_PATH, self.embeddings, allow_dangerous_deserialization=True
        )
