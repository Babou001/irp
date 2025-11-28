from redis import Redis, ConnectionPool
import json
import os
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from datetime import datetime, timezone

def create_redis_client():
    redis_host = os.getenv('REDIS_HOST', '127.0.0.1')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    pool = ConnectionPool(host=redis_host, port=redis_port, max_connections=100, decode_responses=True)
    return Redis(connection_pool=pool)

class RedisChatMessageHistory:
    """
    Historique des messages d'une session via Redis, avec prise en charge
    de la durée des réponses assistant et TTL glissant optionnel.
    """
    def __init__(self, session_id: str, redis_client: Redis, ttl_seconds: int | None = None):
        self.session_id = session_id
        self.redis_client = redis_client
        self.key = f"chat_history:{session_id}"
        self.ttl_seconds = ttl_seconds

    def _push(self, data: dict):
        self.redis_client.rpush(self.key, json.dumps(data))
        if self.ttl_seconds:
            # TTL "glissant" : on renouvelle à chaque insertion
            self.redis_client.expire(self.key, self.ttl_seconds)

    def get_messages(self):
        """Reconstruit des objets LangChain à partir du JSON stocké."""
        messages = []
        for message_json in self.redis_client.lrange(self.key, 0, -1):
            data = json.loads(message_json)
            role = data.get("role")
            content = data.get("content", "")
            if role == "system":
                msg = SystemMessage(content=content)
            elif role == "assistant":
                msg = AIMessage(content=content)
                if "duration" in data:
                    setattr(msg, "duration", data["duration"])
            else:
                msg = HumanMessage(content=content)
            messages.append(msg)
        return messages

    @property
    def messages(self):
        return self.get_messages()

    def add_message(self, message):
        """Ajoute un message LangChain, en conservant la durée si présente."""
        if isinstance(message, SystemMessage):
            role = "system"
        elif isinstance(message, HumanMessage):
            role = "user"
        elif isinstance(message, AIMessage):
            role = "assistant"
        else:
            role = "unknown"

        data = {
            "role": role,
            "content": message.content,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        dur = getattr(message, "duration", None)
        if dur is not None:
            data["duration"] = float(dur)
        self._push(data)

    def add_ai_message(self, content: str, duration: float | None = None):
        """Utilitaire explicite pour les réponses assistant."""
        data = {
            "role": "assistant",
            "content": content,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        if duration is not None:
            data["duration"] = float(duration)
        self._push(data)

    def clear(self):
        self.redis_client.delete(self.key)

def get_chat_history(redis_cl, session_id: str, ttl_seconds: int | None = None) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(session_id, redis_cl, ttl_seconds=ttl_seconds)
