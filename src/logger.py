
import json
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "hr_chatbot_logs.jsonl"


def log_interaction(question, retrieved_chunks, answer):

    # Create logs folder if it doesn't exist
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Prepare interaction details
    log_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "retrieved_chunks": [
            {
                "source": chunk["source"],
                "content": chunk["content"],
                "distance": chunk["distance"]
            }
            for chunk in retrieved_chunks
        ],
        "answer": answer
    }

    # Append interaction to the log file
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(log_data, ensure_ascii=False) + "\n")

    print("Interaction logged successfully!")
