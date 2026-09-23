from datetime import datetime, timezone
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
AUDIT_FILE = BASE_DIR / "logs" / "audit.jsonl"


def log_event(event: dict):
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **event,
    }

    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
