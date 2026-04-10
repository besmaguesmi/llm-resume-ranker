import os
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # free
LLM_MODEL = "google/flan-t5-large"  # free, or use "mistralai/Mistral-7B-Instruct-v0.1"
VECTOR_STORE_PATH = "faiss_index"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 5  # number of top resumes to return
