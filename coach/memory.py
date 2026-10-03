import json
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "data" / "memory.json"
EMPTY = {"profile": [], "goals": [], "commitments": [], "notes": ""}


def load() -> dict:
    try:
        return json.loads(PATH.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(EMPTY)


def save(memory: dict) -> None:
    PATH.parent.mkdir(exist_ok=True)
    PATH.write_text(json.dumps(memory, indent=2))
