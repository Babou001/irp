# -*- coding: utf-8 -*-
"""
preprocess.py — ingestion RAG avec Milvus (ta fonction d'extraction + skip TOC conservateur)

- TA fonction extract_text_with_layout est intégrée telle quelle (PyMuPDF)
- is_skippable_page : heuristique CONSERVATRICE (ne skippe que si en-tête explicite)
- get_text() renvoie toujours (text, meta)
- chunking: 1200/150
- normalisation des métadonnées (title/source toujours présents, tout en str)
- insertion Milvus par fichier (continue si un PDF échoue)

CLI:
    python preprocess.py preprocess   # indexe tout 'data/'
    python preprocess.py add_doc      # ingère les nouveaux PDFs depuis 'uploads/'
"""

from __future__ import annotations

import os
import re
import sys
import pickle
import shutil
from typing import List, Tuple, Dict, Any
from collections import defaultdict

# ---- LangChain
try:
    from langchain_core.documents import Document
except Exception:
    from langchain.schema import Document  # type: ignore

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ---- Milvus
from pymilvus import utility, Collection
from pymilvus.exceptions import MilvusException, DataNotMatchException

# ---- Modules locaux
import paths
import retriever

from pymilvus import Collection, DataType
from langchain_milvus import Milvus as LCMilvus  


# =========================
# TA FONCTION D'EXTRACTION (ET HELPERS)
# =========================

# Dépendance requise : pip install "pymupdf>=1.24.0"
import fitz  # PyMuPDF

def load_doc(filepath: str):
    """Ouvre le PDF avec PyMuPDF; renvoie l'objet doc ou None en cas d'échec."""
    try:
        return fitz.open(filepath)
    except Exception as e:
        print(f"[PDF][FAIL] cannot open {filepath}: {e}")
        return None

def is_skippable_page(plain_txt: str) -> bool:
    """
    Heuristique CONSERVATRICE pour ignorer Table of Contents / Revision History.
    - On regarde uniquement le DÉBUT de la page (500 premiers caractères).
    - On cherche des entêtes explicites ; PAS de tests '....' ni du substring 'toc'.
    """
    if not plain_txt:
        return False
    head = plain_txt.strip()[:500].lower()
    headings = (
        "table of contents",
        "sommaire",
        "table des matières",
        "revision history",
        "historique des révisions",
        "change log",
        "document history",
    )
    return any(h in head for h in headings)

def strip_sections(text: str) -> str:
    """Nettoyage léger optionnel des sections; ici on garde simple."""
    return text.strip()

def extract_text_with_layout(
    filepath,
    images_dir="images",
    space_multiplier=0.5,
):
    """Extract text with rudimentary layout, skipping TOC/History pages."""
    doc = load_doc(filepath)
    if doc is None:
        return ""

    meta = doc.metadata

    os.makedirs(images_dir, exist_ok=True)
    full_lines = []

    for pno in range(doc.page_count):
        page = doc.load_page(pno)

        #   decide early whether we keep this page
        plain_txt = page.get_text("text")
        if is_skippable_page(plain_txt):
            print(f"Skipping page {pno + 1} (TOC / history)")
            continue  # jump to next page

        # page delimiter (only for retained pages)
        full_lines.append(f"--- Page {pno + 1} ---")

        page_dict = page.get_text("dict")

        # text blocks, top-to-bottom
        blocks = sorted(page_dict.get("blocks", []), key=lambda b: b['bbox'][1])
        for block in blocks:
            # process lines within block
            lines = sorted(block.get("lines", []), key=lambda l: l['bbox'][1])
            for line in lines:
                spans = sorted(line.get("spans", []), key=lambda s: s['bbox'][0])
                line_text = ""
                cursor_x = None
                for span in spans:
                    x0, _, x1, _ = span['bbox']
                    txt = span.get('text', '')
                    if cursor_x is not None:
                        gap = x0 - cursor_x
                        n_spaces = max(1, int(gap // (span['size'] * space_multiplier)))
                        line_text += ' ' * n_spaces
                    line_text += txt
                    cursor_x = x1
                full_lines.append(line_text.rstrip())
            # blank line after block
            full_lines.append("")

    doc.close()

    # join lines & collapse 3+ newlines to 2
    text = "\n".join(full_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return strip_sections(text), meta

def get_text(path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Utilise TA fonction ci-dessus.
    Elle peut dans un cas retourner juste "" (string) si doc=None ; on enveloppe pour
    toujours renvoyer (text, meta: dict).
    """
    try:
        res = extract_text_with_layout(path)
        if isinstance(res, tuple):
            text, meta = res
            return text or "", (meta or {})
        else:
            return str(res) or "", {}
    except Exception as e:
        print(f"[EXTRACT][FAIL] {path}: {e}")
        return "", {}

# =========================
# Config & utilitaires
# =========================

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 150

def get_all_files() -> List[str]:
    """Liste tous les PDF du corpus 'data/'."""
    base = getattr(paths, "data_path", "data")
    if not os.path.exists(base):
        return []
    files = []
    for name in os.listdir(base):
        f = os.path.join(base, name)
        if os.path.isfile(f) and name.lower().endswith(".pdf"):
            files.append(os.path.abspath(f))
    return sorted(files)

def sanitize_filename(name: str) -> str:
    name = os.path.basename(name)
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name)

# =========================
# Chunking
# =========================

def get_chunks(chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[Document]:
    """Découpe tous les PDF du corpus en chunks Document(page_content, metadata)."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    docs: List[Document] = []
    files = get_all_files()

    for fpath in files:
        text, meta = get_text(fpath)
        if not text:
            print(f"[READ][SKIP] empty text: {fpath}")
            continue
        meta_clean = {k: v for k, v in (meta or {}).items() if v is not None}
        meta_clean = {str(k): str(v) for k, v in meta_clean.items()}
        meta_clean["source"] = os.path.abspath(fpath)
        if not meta_clean.get("title"):
            meta_clean["title"] = os.path.splitext(os.path.basename(fpath))[0]
        docs.append(Document(page_content=text, metadata=meta_clean))

    all_splits = text_splitter.split_documents(docs)

    # Sauvegarde pickle (debug)
    directory_path = getattr(paths, "chunks_dir_path", os.path.join("preprocessed", "chunks"))
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, "all_splits.pkl")
    try:
        with open(file_path, "wb") as f:
            pickle.dump(all_splits, f)
    except Exception as e:
        print(f"[SAVE][WARN] cannot dump chunks to {file_path}: {e}")

    return all_splits

# =========================
# Normalisation & insertion résiliente (Milvus)
# =========================

def _normalize_doc_metadata(docs: List[Document]) -> List[Document]:
    """
    Milvus fige le schéma au 1er insert. Pour éviter 'Insert missed field ...':
      - cast toutes les valeurs en str
      - assure 'source' et 'title'
      - remplit les clés manquantes avec ""
    """
    all_keys = set()
    for d in docs:
        md = d.metadata or {}
        d.metadata = {str(k): ("" if v is None else str(v)) for k, v in md.items()}
        all_keys.update(d.metadata.keys())

    all_keys.update({"source", "title"})

    for d in docs:
        if not d.metadata.get("source"):
            d.metadata["source"] = ""
        if not d.metadata.get("title"):
            base = os.path.splitext(os.path.basename(d.metadata.get("source", "")))[0]
            d.metadata["title"] = base or "untitled"

    for d in docs:
        for k in all_keys:
            if k not in d.metadata:
                d.metadata[k] = ""

    return docs

def _group_by_source(docs: List[Document]) -> Dict[str, List[Document]]:
    groups: Dict[str, List[Document]] = defaultdict(list)
    for d in docs:
        src = d.metadata.get("source") or "unknown"
        groups[src].append(d)
    return groups




def _normalize_docs_for_collection(vectorstore, collection_name, docs):
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


def _safe_add_per_source(vectorstore, splits: List[Document]) -> Tuple[int, List[str]]:
    """
    Insert par fichier. Si un fichier échoue, on le logge et on continue.
    Retourne (n_inserted, failed_sources[list]).
    """
    inserted, failed = 0, []
    groups = _group_by_source(splits)
    for src, docs in groups.items():
        try:
            docs = _normalize_doc_metadata(docs)
            docs = _normalize_docs_for_collection(vectorstore, getattr(paths, "MILVUS_COLLECTION", "rag_docs"), docs)
            vectorstore.add_documents(docs)  # Milvus auto-id
            inserted += len(docs)
        except (DataNotMatchException, MilvusException, Exception) as e:
            print(f"[Milvus][SKIP] insertion failed for source: {src}\n  -> {e}")
            failed.append(src)
    return inserted, failed

# =========================
# Vectorizer (Milvus)
# =========================

def get_vectorizer(
    save_path: str = getattr(paths, "preprocessed_data", "preprocessed"),
    collection_name: str = getattr(paths, "MILVUS_COLLECTION", "rag_docs"),
    host: str = getattr(paths, "MILVUS_HOST", "127.0.0.1"),
    port: int = int(getattr(paths, "MILVUS_PORT", 19530)),
) -> Any:
    """
    Ouvre/crée la collection Milvus et la peuple si vide.
    Retourne un vectorstore LangChain (Milvus).
    """
    embedding_model = HuggingFaceEmbeddings(model_name=paths.bert_model_path)
    vectorstore = retriever.load_vectorstore(embedding_model, collection_name=collection_name)

    # Est-ce que la collection existe / contient des entités ?
    try:
        if not utility.has_collection(collection_name):
            raise MilvusException(message=f"Collection '{collection_name}' not exist, or schema not ready.")

        col = Collection(collection_name)
        try:
            col.load()
        except Exception as e:
            print(f"[Milvus][WARN] load() failed for '{collection_name}': {e}")
        n = getattr(col, "num_entities", 0)
    except Exception as e:
        print(f"[Milvus] Collection lookup failed ({e}) — treating as empty.")
        n = 0

    # Peupler si vide
    if n == 0:
        print(f"[Milvus] Creating collection <{collection_name}> and embedding all documents …")
        all_splits = get_chunks(chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
        if all_splits:
            # 1) uniformiser les métadatas pour un schéma stable
            all_splits = _normalize_doc_metadata(all_splits)

            # 2) création *explicite* de la collection + insert initial
            try:
                vectorstore = LCMilvus.from_documents(
                    documents=all_splits,
                    embedding=embedding_model,                        # NB: param s’appelle 'embedding'
                    connection_args={"uri": paths.MILVUS_URI},        # <<— URI
                    collection_name=collection_name,
                    index_params={"index_type": "HNSW", "metric_type": "COSINE", "params": {"M": 16, "efConstruction": 200}},
                    search_params={"metric_type": "COSINE", "params": {"ef": 128}},
                    drop_old=False,
                )
                print(f"[Milvus] Inserted {len(all_splits)} chunks (new collection).")
            except Exception as e:
                print(f"[Milvus][ERROR] initial creation failed: {e}")
        else:
            print("[Milvus] No chunks to insert (corpus empty?).")
    else:
        print(f"[Milvus] Using existing collection <{collection_name}> ({n} vectors)")

    return vectorstore

# =========================
# Ajout de nouveaux documents depuis 'uploads/'
# =========================

def add_documents(
    upload_directory: str = getattr(paths, "upload_dir_path", "uploads"),
    collection_name: str = getattr(paths, "MILVUS_COLLECTION", "rag_docs"),
    host: str = getattr(paths, "MILVUS_HOST", "127.0.0.1"),
    port: int = int(getattr(paths, "MILVUS_PORT", 19530)),
) -> None:
    """
    Embeds only the *new* PDFs present in `upload_directory`
    and appends them to the Milvus collection.
    """
    try:
        existing_files = set(os.listdir(paths.data_path)) if os.path.exists(paths.data_path) else set()
        new_files = [f for f in os.listdir(upload_directory) if f.lower().endswith(".pdf") and f not in existing_files]

        if not new_files:
            print("No new documents to process.")
            return

        print(f"Processing {len(new_files)} new documents …")

        splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        new_docs: List[Document] = []
        for fname in new_files:
            fpath = os.path.join(upload_directory, fname)
            try:
                text, meta = get_text(fpath)
                if not text:
                    print(f"[READ][SKIP] empty text: {fpath}")
                    continue
                meta_clean = {k: v for k, v in (meta or {}).items() if v is not None}
                meta_clean = {str(k): str(v) for k, v in meta_clean.items()}
                meta_clean["source"] = os.path.abspath(os.path.join(paths.data_path, fname))
                if not meta_clean.get("title"):
                    meta_clean["title"] = os.path.splitext(os.path.basename(meta_clean["source"]))[0]
                new_docs.append(Document(page_content=text, metadata=meta_clean))
            except Exception as e:
                print(f"[READ][SKIP] failed to parse {fpath}: {e}")

        if not new_docs:
            print("No readable text found in the uploaded files.")
            return

        new_splits = splitter.split_documents(new_docs)

        # Append résilient par fichier
        embedding_model = HuggingFaceEmbeddings(model_name=paths.bert_model_path)
        vectorstore = retriever.load_vectorstore(embedding_model, collection_name=collection_name)
        n, failed = _safe_add_per_source(vectorstore, new_splits)
        print(f"Added {n} chunks from {len(new_docs)} file(s) to Milvus.")
        if failed:
            print("[Milvus] The following sources failed and were skipped:")
            for s in failed:
                print("  -", s)

        # Déplacer vers data/
        for fname in new_files:
            try:
                shutil.move(
                    os.path.join(upload_directory, fname),
                    os.path.join(paths.data_path, fname)
                )
            except Exception as e:
                print(f"[MOVE][WARN] {fname} -> {paths.data_path}: {e}")

    except Exception as e:
        print(f"[ADD][ERROR] {e}")

# =========================
# CLI
# =========================

def _usage():
    print("Usage:")
    print("  python preprocess.py preprocess   # indexe tout le dossier data/")
    print("  python preprocess.py add_doc      # ingère les nouveaux PDF depuis uploads/")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        _usage()
        sys.exit(0)

    cmd = sys.argv[1].strip().lower()
    if cmd == "preprocess":
        get_vectorizer()
    elif cmd == "add_doc":
        add_documents()
    else:
        _usage()
