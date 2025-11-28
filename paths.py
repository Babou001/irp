import os

# Base directory (current file's location)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Data directories
data_path = os.path.join(base_dir, "data")
preprocessed_data = os.path.join(base_dir, "preprocessed_data")
upload_dir_path = os.path.join(base_dir, "uploads")
chunks_dir_path = os.path.join(preprocessed_data, "chunks")

# model encoder for text
bert_model_path = os.path.join(base_dir, "models" , "all-mpnet-base-v2")


# Model path: Set via environment variable or default to a predefined model
default_model = "Llama-3.2-3B-Instruct-Q5_K_L.gguf"  # Using Q5 (better quality than Q4)
generator_model_path = os.getenv("GENERATOR_MODEL_PATH", os.path.join(base_dir, "models", default_model))

# explanation video
exp_video = os.path.join(base_dir, "videos", "view_doc_explanation.mp4")

# Path to FAISS index
faiss_index_path = os.path.join(preprocessed_data, "Faiss_index", "optimized_faiss.index")
"""
# Ensure required directories exist
for path in [data_path, preprocessed_data, upload_dir_path, chunks_dir_path, os.path.dirname(faiss_index_path)]:
    os.makedirs(path, exist_ok=True)
"""

# Image logo
image_logo = os.path.join(base_dir, "images", "test.png")


# -------- Milvus config --------
MILVUS_HOST = os.getenv("MILVUS_HOST", "127.0.0.1")
MILVUS_PORT = int(os.getenv("MILVUS_PORT", "19530"))
MILVUS_URI  = os.getenv("MILVUS_URI", f"http://{MILVUS_HOST}:{MILVUS_PORT}")  # certains wrappers acceptent http/grpc
MILVUS_COLLECTION = os.getenv("MILVUS_COLLECTION", "rag_docs")
# Dimension des embeddings (all-mpnet-base-v2 = 768)
EMB_DIM = 768


# streamlit run streamlit_app.py --browser.serverAddress localhost
# uvicorn fast_api_app:app --host 0.0.0.0 --port 8000 --workers 1
# chroma run --path ./chroma_langchain_db --port 8010