import json
from pathlib import Path

FILE_PATH = Path("user_messages.json")

def load_messages():
    if not FILE_PATH.exists():
        return []
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_messages(messages):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def add_message(user_id, user_name, message_text):
    messages = load_messages()
    new_id = (max([m["id"] for m in messages]) + 1) if messages else 1
    messages.append({
        "id": new_id,
        "user_id": user_id,
        "user_name": user_name,
        "message": message_text,
        "answered": False,
        "answer": ""
    })
    save_messages(messages)
    return new_id

def update_message_answer(message_id, answer_text):
    messages = load_messages()
    for m in messages:
        if m["id"] == message_id:
            m["answered"] = True
            m["answer"] = answer_text
            break
    save_messages(messages)
