from datetime import datetime
import pathlib
import tag_manager


BASE_DIR = pathlib.Path(__file__).parent
NOTES_DIR = BASE_DIR / "notes"

def save(content: str) -> None:
    today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = NOTES_DIR / f"{today}.md"
    with open(file_name, "x", encoding="utf-8") as f:
        f.write(content)
    new_tags = {tag: [str(file_name)] for tag in tag_manager.extract_tags(content)}
    tag_manager.update_tags(new_tags)
    