"""
retriever.py — Milvus-based vector store + retriever utilities

Remplace l'implémentation Chroma par Milvus, tout en conservant
les mêmes fonctions publiques :

- load_vectorstore(embedding_model, collection_name="rag_docs")
- get_retriever(vectorstore, k=NB_DOCS)
- get_best_files(query: str, retriever, k=NB_DOCS) -> (paths, metas)

Prérequis:
    pip install pymilvus>=2.4.0
    pip install langchain-milvus  # ou fallback langchain_community

Configuration (dans paths.py ou via variables d'environnement):
    MILVUS_HOST (def: "localhost")
    MILVUS_PORT (def: "19530")
    MILVUS_COLLECTION (def: "rag_docs")
"""

from __future__ import annotations

import os
import asyncio
from typing import List, Tuple, Any

import paths

# Milvus vectorstore wrapper (utilise langchain-milvus si dispo, sinon community)
try:
    from langchain_milvus import Milvus
except Exception:  # pragma: no cover - fallback
    from langchain_community.vectorstores import Milvus  # type: ignore

from pymilvus import connections  # pour init la connexion
from typing import Any, Optional

# Import VectorStoreRetriever (nouvelle API LangChain)
try:
    from langchain_core.vectorstores import VectorStoreRetriever
except ImportError:
    try:
        from langchain.vectorstores.base import VectorStoreRetriever
    except ImportError:
        # Fallback si aucun des deux ne fonctionne
        VectorStoreRetriever = None

try:
    from langchain_core.runnables import RunnableConfig
except Exception:
    from langchain_core.runnables.config import RunnableConfig



# Nombre de documents à retourner par défaut
NB_DOCS = 2


def _get_milvus_cfg() -> Tuple[str, str, str]:
    """Lit la config Milvus depuis paths.py (si définie) ou depuis l'environnement."""
    host = getattr(paths, "MILVUS_HOST", os.getenv("MILVUS_HOST", "localhost"))
    port = str(getattr(paths, "MILVUS_PORT", os.getenv("MILVUS_PORT", "19530")))
    collection = getattr(paths, "MILVUS_COLLECTION", os.getenv("MILVUS_COLLECTION", "rag_docs"))
    return host, port, collection


def load_vectorstore(embedding_model: Any, collection_name: str | None = None) -> Milvus:
    """
    Initialise (ou ouvre) une collection Milvus pour le RAG.

    Args:
        embedding_model: instance d'Embeddings LangChain (ex: HuggingFaceEmbeddings)
        collection_name: nom de la collection Milvus (optionnel)

    Returns:
        Milvus vectorstore (LangChain)
    """
    host, port, default_collection = _get_milvus_cfg()
    collection_name = collection_name or default_collection

    # Connexion gRPC (langchain utilise pymilvus derrière)
    # Note: langchain_milvus.Milvus expects 'uri' in connection_args
    connections.connect(alias="default", host=host, port=port)

    # Bon compromis pour mpnet (COSINE) — ajustables si besoin
    index_params = {
        "index_type": "HNSW",
        "metric_type": "COSINE",
        "params": {"M": 16, "efConstruction": 200},
    }
    search_params = {"metric_type": "COSINE", "params": {"ef": 128}}

    # Build URI for Milvus connection
    milvus_uri = f"http://{host}:{port}"

    vs = Milvus(
        embedding_function=embedding_model,
        collection_name=collection_name,
        connection_args={"uri": milvus_uri},  # Use URI instead of separate host/port
        # Les champs ci-dessous sont standardisés par les wrappers récents
        text_field="text",
        vector_field="vector",
        auto_id=True,
        index_params=index_params,
        search_params=search_params,
    )
    return vs


class VectorStoreRetrieverK(VectorStoreRetriever):
    """VectorStoreRetriever avec un 'k' contrôlé dynamiquement."""
    actual_k: int = NB_DOCS  # garde ta constante / valeur par défaut

    def _apply_k(self):
        try:
            k = int(self.actual_k)
        except Exception:
            k = None
        if k and k > 0:
            # search_kwargs est ce que lit VectorStoreRetriever
            self.search_kwargs = {**(getattr(self, "search_kwargs", {}) or {}), "k": k}
            # certains backends regardent aussi un attribut .k si présent
            try:
                self.k = k
            except Exception:
                pass

    def invoke(self, input: Any, config: Optional[RunnableConfig] = None):
        self._apply_k()
        return super().invoke(input, config=config)

    async def ainvoke(self, input: Any, config: Optional[RunnableConfig] = None):
        self._apply_k()
        return await super().ainvoke(input, config=config)


def get_retriever(vectorstore: Any, k: int = NB_DOCS) -> VectorStoreRetrieverK:
    """
    Construit un retriever LangChain à partir du vectorstore Milvus.
    """
    return VectorStoreRetrieverK(
        vectorstore=vectorstore,
        k=k,
        search_kwargs={"k": k},
        # search_type="similarity"  # (par défaut)
    )


async def get_best_files(query: str, retriever: VectorStoreRetrieverK, k: int = NB_DOCS) -> Tuple[List[str], List[dict]]:
    """
    Lance une recherche via le retriever et renvoie (list_paths, list_metas).

    Args:
        query: requête utilisateur
        retriever: retriever renvoyé par get_retriever(...)
        k: nombre de documents à retourner

    Returns:
        (doc_paths, metas)
    """
    # Forcer k au cas où l'appelant change la valeur
    retriever.actual_k = k
    docs = await retriever.ainvoke(query)

    doc_paths = [d.metadata.get("source") for d in docs]
    metas = [d.metadata for d in docs]
    return doc_paths, metas


def parse_retriever_input(x: Any) -> str:
    """Extrait la requête utilisateur depuis divers formats."""
    if isinstance(x, str):
        return x

    if isinstance(x, dict):
        for key in ("question", "query", "input"):
            if key in x and isinstance(x[key], str):
                return x[key]

        # Historique de chat (list LC messages ou dicts)
        if "messages" in x:
            msgs = x["messages"]
            try:
                seq = list(msgs) if isinstance(msgs, (list, tuple)) else []
                # cherche la dernière entrée humaine
                for m in reversed(seq):
                    # LangChain Message
                    if hasattr(m, "type") and getattr(m, "type") == "human":
                        return getattr(m, "content", str(m)) or ""
                    # dict {type/role/content}
                    if isinstance(m, dict) and (m.get("type") == "human" or m.get("role") == "user"):
                        return (m.get("content") or "").strip()
                # fallback: contenu du dernier élément
                last = seq[-1] if seq else ""
                if hasattr(last, "content"):
                    return getattr(last, "content") or ""
                if isinstance(last, dict):
                    return (last.get("content") or "") if last else ""
                return str(last)
            except Exception:
                return str(x)

    # fallback robuste
    return str(x)