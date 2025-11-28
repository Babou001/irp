import paths
import redis_db
from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.messages import HumanMessage, SystemMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Import create_stuff_documents_chain (nouvelle API LangChain)
try:
    from langchain.chains.combine_documents import create_stuff_documents_chain
except ImportError:
    try:
        from langchain_core.chains import create_stuff_documents_chain
    except ImportError:
        # Fallback - on définira une version simplifiée si nécessaire
        create_stuff_documents_chain = None

import asyncio, time
from datetime import datetime
import os
from typing import List, Optional



# Initialize Redis Client
redis_client = redis_db.create_redis_client()

class SourceRenderer:
    """
    Formate une liste de Documents (retriever) en section 'Sources' :
    - Déduplication prioritaire par 'source' (un PDF = une ligne)
      puis 'pk' si 'source' est absent, sinon titre+auteur.
    - Affiche: Titre — Auteur — Date — `NomDuFichier.pdf`
    - Parse les dates PDF de type 'D:YYYYMMDDHHmmSS+TZ'
    - Limite d'affichage: MAX_SOURCES (par défaut 5)
    """
    MAX_SOURCES = 5  # ↔ augmente à 10/None selon besoin

    def __init__(self, docs: List):
        self.docs = docs or []

    @staticmethod
    def _parse_pdf_date(raw: Optional[str]) -> Optional[str]:
        if not raw:
            return None
        s = raw.strip()
        if s.startswith("D:"):
            s = s[2:]
        # On garde YYYYMMDD si présent
        if len(s) >= 8 and s[:8].isdigit():
            y = int(s[0:4]); m = int(s[4:6]); d = int(s[6:8])
            if 1 <= m <= 12 and 1 <= d <= 31:
                return f"{y:04d}-{m:02d}-{d:02d}"
        return None

    @staticmethod
    def _pick_title(meta: dict, fallback: str) -> str:
        for k in ("title", "subject"):
            v = (meta.get(k) or "").strip()
            if v:
                return v
        return fallback

    @staticmethod
    def _basename(path: Optional[str]) -> str:
        if not path:
            return ""
        return os.path.basename(path)

    @staticmethod
    def _norm_source(path: Optional[str]) -> Optional[str]:
        if not path:
            return None
        try:
            # Normalise le chemin et insensibilité à la casse (Windows-friendly)
            return os.path.normpath(path).casefold()
        except Exception:
            return path

    def render(self) -> str:
        seen = set()
        items: List[str] = []

        for d in self.docs:
            meta = getattr(d, "metadata", {}) or {}

            # --- Clé de déduplication (PRIORITÉ À 'source') ---
            source_norm = self._norm_source(meta.get("source"))
            if source_norm:
                key = ("source", source_norm)
            elif meta.get("pk") is not None:
                key = ("pk", str(meta["pk"]))
            else:
                key = ("sig", ((meta.get("title") or "").strip(), (meta.get("author") or "").strip()))

            if key in seen:
                continue
            seen.add(key)

            # --- Affichage ---
            fname = self._basename(meta.get("source") or "")
            base = os.path.splitext(fname)[0] or "Document"
            title = self._pick_title(meta, base)
            author = (meta.get("author") or "").strip() or None
            date = self._parse_pdf_date(meta.get("creationDate") or meta.get("modDate"))

            parts = [title]
            tail = []
            if author:
                tail.append(author)
            if date:
                tail.append(date)
            if fname:
                tail.append(f"`{fname}`")

            label = " — ".join(parts + tail) if tail else parts[0]
            items.append(label)

            if self.MAX_SOURCES and len(items) >= self.MAX_SOURCES:
                break

        if not items:
            return ""

        lines = ["", "", "**Sources**:"]
        for i, label in enumerate(items, 1):
            lines.append(f"{i}. {label}")
        return "\n".join(lines)


def get_model():
    """Creates and returns the LlamaCpp model."""
    llm_langchain = ChatLlamaCpp(
        model_path=paths.generator_model_path,
        n_ctx=50000,
        temperature=0.01,
        max_tokens=512,
        top_p=1,
        n_threads=2
    )
    return llm_langchain




def get_chain_generator(generator):
    """Creates the retrieval and response generation pipeline."""
    SYSTEM_TEMPLATE = """
        Answer the user's questions based on the below context. 
        If the context doesn't contain relevant information, just say "I don't know".

        <context>
        {context}
        </context>
    """

    question_answering_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_TEMPLATE),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    document_chain = create_stuff_documents_chain(generator, question_answering_prompt)
    return document_chain




def get_chat_hist_instance(session_id):
    """Fetches chat history from Redis for the given session."""
    return redis_db.get_chat_history(redis_client, session_id)




async def generate_chat_st(user_input, generator_chain, chat_history_instance):
    """
    Génère la réponse + section 'Sources' basée sur les métadonnées des Documents.
    """
    system_prompt_content = (
        "You are a highly helpful assistant, and your name is llama_chat. "
        "Your answers will be concise and direct. "
        "If the provided context lacks relevant information, you may answer without it."
    )

    # 1) System unique
    if not any(isinstance(msg, SystemMessage) for msg in chat_history_instance.messages):
        chat_history_instance.add_message(SystemMessage(content=system_prompt_content))

    # 2) Message utilisateur
    chat_history_instance.add_message(HumanMessage(content=user_input))

    # 3) Trim de l'historique (~4000 caractères)
    history = trim_messages(
        chat_history_instance.messages,
        strategy="last",
        start_on="human",
        end_on=("human", "tool"),
        token_counter=len,
        include_system=True,
        max_tokens=4000,
    )

    # 4) Appel du chain (ici: retriever_chain)
    start = time.time()
    pack = await asyncio.ensure_future(generator_chain.ainvoke({"messages": history}))
    elapsed = time.time() - start

    # Réponse LLM
    response = pack.get("answer") if isinstance(pack, dict) else str(pack)

    # 5) Construction de la section 'Sources'
    docs = pack.get("context", []) if isinstance(pack, dict) else []
    sources_block = SourceRenderer(docs).render()
    final_text = response + sources_block if sources_block else response

    # 6) Persistance via la classe unifiée (inclut duration)
    chat_history_instance.add_ai_message(final_text, duration=elapsed)

    # 7) Métriques dashboard
    date_str = datetime.utcnow().date().isoformat()
    chat_history_instance.redis_client.rpush(f"response_times:{date_str}", elapsed)
    chat_history_instance.redis_client.incr(f"responses:{date_str}")

    return chat_history_instance, elapsed


