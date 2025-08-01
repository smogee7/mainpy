from datetime import datetime

def log_purchase(username: str):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("data/buyers_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{time} — {username}\n")