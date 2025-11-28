from fastapi import FastAPI, UploadFile, File
import retriever as rt
import generator
import paths
import redis_db
import os
import asyncio
from langchain_huggingface import HuggingFaceEmbeddings
import json
import preprocess
from langchain_core.documents import Document

# Import RecursiveCharacterTextSplitter (nouvelle API LangChain)
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

import asyncio, shutil
from uuid import uuid4
from typing import Literal
from pydantic import BaseModel
import re
from fastapi.responses import JSONResponse
from langchain_core.runnables import RunnablePassthrough
from retriever import parse_retriever_input
from pymilvus import Collection, DataType
from collections import Counter



app = FastAPI()
MAX_PDF_MB = 25


vectorstore_lock = asyncio.Lock()          # protects concurrent writes


# Global chat queue, worker tasks, and a lock to serialize model calls
chat_queue = asyncio.Queue()
worker_tasks = []
model_lock = asyncio.Lock()  # Ensures only one model call is active at a time

# ===== LAZY LOADING: Models are loaded on first use, not at startup =====
# This prevents file locking issues in Docker with mounted volumes
embedding_model = None
vectorstore = None
generator_model = None
generator_chain = None
lc_retriever = None
retriever_chain = None
redis_client = None

# Lock to ensure models are initialized only once
_models_init_lock = asyncio.Lock()
_models_initialized = False


async def _ensure_models_loaded():
    """
    Lazy initialization of models on first API call.
    This avoids macOS Docker volume file locking issues at container startup.
    """
    global embedding_model, vectorstore, generator_model, generator_chain
    global lc_retriever, retriever_chain, redis_client, _models_initialized

    async with _models_init_lock:
        if _models_initialized:
            return

        print("🔄 Initializing models (lazy loading)...")

        # Load embedding model
        embedding_model = HuggingFaceEmbeddings(model_name=paths.bert_model_path)

        # Load vectorstore
        vectorstore = rt.load_vectorstore(embedding_model)

        # Load generator model
        generator_model = generator.get_model()
        generator_chain = generator.get_chain_generator(generator_model)

        # Create retriever
        lc_retriever = rt.get_retriever(vectorstore, k=2)
        retriever_chain = RunnablePassthrough.assign(
            context=parse_retriever_input | lc_retriever
        ).assign(answer=generator_chain)

        # Redis client
        redis_client = redis_db.create_redis_client()

        _models_initialized = True
        print("✅ Models initialized successfully!")



def sanitize_filename(name: str) -> str:
    name = os.path.basename(name)
    return re.sub(r'[^A-Za-z0-9._-]+', '_', name)

@app.on_event("startup")
async def startup_event():
    global worker_tasks
    num_workers = 1  # Adjust the number of workers as needed
    for _ in range(num_workers):
        task = asyncio.create_task(chat_worker())
        worker_tasks.append(task)


@app.on_event("shutdown")
async def shutdown_event():
    for task in worker_tasks:
        task.cancel()
    await asyncio.gather(*worker_tasks, return_exceptions=True)


async def chat_worker():
    """Worker that continuously processes chat requests from the queue."""
    while True:
        session_id, user_input, future = await chat_queue.get()
        try:
            chat_hist = generator.get_chat_hist_instance(session_id)
            # Serialize access to the generator chain to avoid connection issues
            async with model_lock:
                chat_hist , duration = await generator.generate_chat_st(user_input, retriever_chain, chat_hist)
            result = ( chat_hist.messages[-1].content , duration )
            future.set_result(result)
        except Exception as e:
            future.set_exception(e)
        finally:
            chat_queue.task_done()


@app.get("/")
async def home():
    return {"message": "FastAPI is running!"}


class RetrievePayload(BaseModel):
    query: str
    mode: Literal["vector", "words"] | None = None  # pour validation/évolution future



def _dedupe_by_source(paths, metas):
    """
    Garde un seul résultat par document (clé=metadata['source'] si dispo, sinon le path).
    Conserve l'ordre: on garde la première occurrence (la plus pertinente).
    """
    seen = set()
    out_paths, out_metas = [], []
    for p, m in zip(paths or [], metas or []):
        m = m or {}
        key = m.get("source") or p
        if key not in seen:
            seen.add(key)
            out_paths.append(p)
            out_metas.append(m)
    return out_paths, out_metas



def _count_hits_by_source(paths, metas):
    """Compte combien de chunks ont matché par document (pour badge '(n hits)')"""
    keys = [(m or {}).get("source") or p for p, m in zip(paths or [], metas or [])]
    return Counter(keys)



@app.post("/retrieve")
async def retrieve_documents(payload: RetrievePayload):
    await _ensure_models_loaded()  # Lazy load models on first call

    # On récupère plus de chunks que nécessaire, puis on déduplique
    UNIQUE_K = 5
    OVERFETCH = 5  # 5x plus de chunks pour obtenir au moins UNIQUE_K docs uniques
    paths, metas = await rt.get_best_files(
        query=payload.query,
        retriever=lc_retriever,
        k=UNIQUE_K * OVERFETCH,
    )

    # Déduplication par document (source)
    hit_counts = _count_hits_by_source(paths, metas)
    paths, metas = _dedupe_by_source(paths, metas)

    # On tronque aux N docs uniques demandés
    paths = paths[:UNIQUE_K]
    metas = metas[:UNIQUE_K]

    # Optionnel: renvoyer le nombre de hits par doc pour l'UI (badge)
    hits = [hit_counts.get(m.get("source") or p, 1) for p, m in zip(paths, metas)]

    return {
        "documents": paths,
        "metadatas": metas,
        "hits": hits,          # <- ton UI peut l'afficher "(n hits)" à côté du nom
    }



@app.post("/chat")
async def chat(user_input: str, session_id: str):
    await _ensure_models_loaded()  # Lazy load models on first call

    # Create a future to hold the result of this chat request
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    # Put the task into the queue
    await chat_queue.put((session_id, user_input, future))
    # Wait for the worker to process the task and return the result
    response , duration = await future
    return {"response": response , "duration" : duration}

# =====================================================================

@app.get("/chat/history")
async def chat_history(session_id: str):
    """
    Récupère l'historique complet (role, content, duration) tel qu'enregistré dans Redis.
    """
    await _ensure_models_loaded()  # Lazy load models on first call

    # on récupère la clé dans generator
    chat_hist = generator.get_chat_hist_instance(session_id)
    key = chat_hist.key  # ex. "chat_history:<session_id>"
    # lrange renvoie les JSON strings {"role","content","duration"?}
    raw = redis_client.lrange(key, 0, -1)
    # reconvertit en liste de dicts
    history = [json.loads(item) for item in raw]
    # on filtre juste les system, si souhaité
    history = [m for m in history if m.get("role") != "system"]
    return {"history": history}




def looks_like_pdf(data: bytes) -> bool:
    """
    Accepte un PDF si l'en-tête '%PDF-' apparaît en tout début,
    en tolérant un BOM UTF-8 et/ou des espaces / NULs initiaux.
    """
    head = data[:1024]  # on se limite au début du fichier
    # Retirer BOM UTF-8 si présent
    if head.startswith(b"\xEF\xBB\xBF"):
        head = head[3:]
    # Tolérer NULs/espaces/retours/onglets avant '%PDF-'
    head = head.lstrip(b"\x00 \t\r\n")
    return head.startswith(b"%PDF-")


def normalize_docs_for_existing_schema(vectorstore, collection_name, docs):
    """
    Aligne docs.metadata sur le schéma EXISTANT de la collection Milvus :
    - garde UNIQUEMENT les champs déjà présents dans la collection
    - remplit les champs manquants avec une valeur par défaut selon dtype
    """
    col = Collection(collection_name)
    # text/vector fields tels que déclarés dans ton vectorstore LangChain
    text_field = getattr(vectorstore, "text_field", "text")
    vector_field = getattr(vectorstore, "vector_field", "vector")
    ignore = {text_field, vector_field, "id", "pk"}

    # map nom_de_champ -> dtype
    schema_map = {f.name: f.dtype for f in col.schema.fields}
    required = [name for name in schema_map.keys() if name not in ignore]

    def default_for(dtype):
        if dtype == DataType.VARCHAR:
            return ""
        if dtype in (DataType.INT8, DataType.INT16, DataType.INT32, DataType.INT64):
            return 0
        if dtype in (DataType.FLOAT, DataType.DOUBLE):
            return 0.0
        if dtype == DataType.BOOL:
            return False
        if dtype == DataType.JSON:
            return {}
        return ""

    def cast_to_dtype(val, dtype):
        try:
            if dtype == DataType.VARCHAR:
                return "" if val is None else str(val)
            if dtype in (DataType.INT8, DataType.INT16, DataType.INT32, DataType.INT64):
                return 0 if val in (None, "") else int(val)
            if dtype in (DataType.FLOAT, DataType.DOUBLE):
                return 0.0 if val in (None, "") else float(val)
            if dtype == DataType.BOOL:
                if isinstance(val, str):
                    return val.strip().lower() in ("true", "1", "yes", "y", "t")
                return bool(val)
            if dtype == DataType.JSON:
                return val if isinstance(val, (dict, list)) else {}
        except Exception:
            return default_for(dtype)
        return val

    norm = []
    for d in docs:
        md = d.metadata or {}
        new_md = {}
        for name in required:
            dtype = schema_map[name]
            if name in md:
                new_md[name] = cast_to_dtype(md.get(name), dtype)
            else:
                new_md[name] = default_for(dtype)
        d.metadata = new_md
        norm.append(d)
    return norm


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    await _ensure_models_loaded()  # Lazy load models on first call

    # 1) Validations de base (mimetype + taille)
    if file.content_type not in {"application/pdf"}:
        return JSONResponse(status_code=400, content={"error": "Only PDF files are accepted."})

    data = await file.read()

    if len(data) > MAX_PDF_MB * 1024 * 1024:
        return JSONResponse(status_code=400, content={"error": f"File too large (> {MAX_PDF_MB} MB)."})

    # 1bis) Vérification contenu PDF (tolérante)
    if not looks_like_pdf(data):
        return JSONResponse(
            status_code=415,
            content={"error": "Invalid PDF file (missing '%PDF-' header near start)."}
        )

    safe_name = sanitize_filename(file.filename)

    # 2) Enregistrement temporaire
    tmp_path = os.path.join(paths.upload_dir_path, safe_name)
    with open(tmp_path, "wb") as f:
        f.write(data)

    # 3) Extraction texte + meta
    text, meta = preprocess.get_text(tmp_path)
    if not text:
        return JSONResponse(status_code=400, content={"error": "Unable to extract text from PDF."})

    meta_clean = {k: v for k, v in (meta or {}).items() if v}
    meta_clean["source"] = os.path.join(paths.data_path, safe_name)

    # 4) Split (chunking harmonisé)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
    docs = splitter.split_documents([Document(page_content=text, metadata=meta_clean)])

    # 5) Embedding + append (protégé par lock)
    async with vectorstore_lock:
        docs = normalize_docs_for_existing_schema(vectorstore, paths.MILVUS_COLLECTION, docs)
        vectorstore.add_documents(docs)

    # 6) Déplacement vers le corpus "data/"
    try:
        shutil.move(tmp_path, os.path.join(paths.data_path, safe_name))
    except Exception as e:
        print(f"Warning: could not move file {safe_name}: {e}")

    return {"message": "File uploaded and indexed.", "filename": safe_name}
