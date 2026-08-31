from collections import defaultdict


conversation_memory = defaultdict(list)


def add_message(session_id: str, role: str, content: str) -> None:
    """
    Add a message to a conversation session.
    """
    conversation_memory[session_id].append({
        "role": role,
        "content": content
    })


def get_history(session_id: str) -> list[dict]:
    """
    Get conversation history for a session.
    """
    return conversation_memory.get(session_id, [])


def clear_history(session_id: str) -> None:
    """
    Clear conversation history for a session.
    """
    conversation_memory.pop(session_id, None)
