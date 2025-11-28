import pytest
from unittest.mock import MagicMock, AsyncMock
from retriever import get_best_files
from redis_db import RedisChatMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

@pytest.mark.asyncio
async def test_get_best_files_vector():
    mock_retriever = MagicMock()
    mock_retriever.ainvoke = AsyncMock(return_value=[
        MagicMock(metadata={"source": "file1.pdf", "foo": 1}),
        MagicMock(metadata={"source": "file2.pdf", "bar": 2}),
    ])
    paths, metas = await get_best_files("test query", mock_retriever, k=2)
    assert paths == ["file1.pdf", "file2.pdf"]
    assert isinstance(metas, list) and len(metas) == 2

def test_redis_chat_message_history():
    mock_redis = MagicMock()
    session_id = "test_session"
    chat_history = RedisChatMessageHistory(session_id, mock_redis)

    chat_history.add_message(HumanMessage(content="Hello"))
    chat_history.add_message(SystemMessage(content="System message"))
    chat_history.add_ai_message("AI response")

    assert mock_redis.rpush.call_count == 3

    mock_redis.lrange.return_value = [
        '{"role": "user", "content": "Hello"}',
        '{"role": "system", "content": "System message"}',
        '{"role": "assistant", "content": "AI response", "duration": 1.23}'
    ]
    messages = chat_history.get_messages()
    assert len(messages) == 3
    assert isinstance(messages[0], HumanMessage)
    assert isinstance(messages[1], SystemMessage)
    assert isinstance(messages[2], AIMessage)
