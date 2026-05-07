from datetime import datetime
import pathlib


BASE_DIR = pathlib.Path(__file__).parent
NOTES_DIR = BASE_DIR / "notes"

def save(content: str) -> None:
    today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"{NOTES_DIR}/{today}-notes.md", "x", encoding="utf-8") as f:
        f.write(content)