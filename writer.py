from datetime import datetime
import pathlib
import tag_manager


BASE_DIR = pathlib.Path(__file__).parent
NOTES_DIR = BASE_DIR / "notes"

def save(content: str) -> None:
    today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    tags = tag_manager.extract_tags(content)

    folder = tags[0] if tags else "general"
    subfolder = None


    if subfolder:
        file_path = NOTES_DIR / folder / subfolder / f"{today}.md"
    else:
        file_path = NOTES_DIR / folder / f"{today}.md"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    print(folder, subfolder)
    with open(file_path, "x", encoding="utf-8") as f:
        f.write(content)
    new_tags = {tag: [str(file_path)] for tag in tag_manager.extract_tags(content)}
    tag_manager.update_tags(new_tags)
    