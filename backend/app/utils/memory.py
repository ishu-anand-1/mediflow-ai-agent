from typing import Dict, List

# 🔥 In-memory store (can replace with Redis later)
memory_store: Dict[str, List[dict]] = {}

# 🔥 Max messages to keep per user
MAX_MEMORY = 10


def get_memory(user_id: str) -> List[dict]:
    """
    📖 Get conversation history
    """
    return memory_store.get(user_id, [])


def save_memory(user_id: str, message: dict):
    """
    💾 Save message to memory
    """

    if user_id not in memory_store:
        memory_store[user_id] = []

    memory_store[user_id].append(message)

    # 🔥 Keep only last N messages
    if len(memory_store[user_id]) > MAX_MEMORY:
        memory_store[user_id] = memory_store[user_id][-MAX_MEMORY:]


def clear_memory(user_id: str):
    """
    🧹 Reset user conversation
    """
    memory_store.pop(user_id, None)