import json
from pathlib import Path
from datetime import datetime

class SimpleLogger:
    def __init__(self, log_file: Path):
        self.log_file = log_file

        # ensure only the DIRECTORY is created, not the file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event: str, payload):
        record = {
            "event": event,
            "payload": payload,
            "timestamp": datetime.now().isoformat()
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
