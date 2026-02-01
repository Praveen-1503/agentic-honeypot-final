from datetime import datetime

conversations = {}

def get_history(conversation_id: str):
    return conversations.get(conversation_id, [])

def add_message(conversation_id: str, role: str, content: str):
    conversations.setdefault(conversation_id, []).append({
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow().isoformat()
    })
