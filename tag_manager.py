import json
import pathlib


TAGS_FILE = pathlib.Path(__file__).parent/"tags"/"tags.json"

def extract_tags(text: str) -> list[str]:
    """Extracts tags from the given text. Tags are defined as words starting with '#'."""
    tags = []
    for word in text.split():
        if word.startswith("#") and not word.startswith("##") and len(word) > 1:
            tags.append(word[1:].strip(",.!?;:()[]{}\"'")) 
    return tags

def load_tags() -> dict[str, list[str]]:
    """Loads tags from the JSON file.
     Returns dict with tag key and path values """
    if not TAGS_FILE.exists():
        return {}
    with open(TAGS_FILE, "r", encoding="utf-8") as f:
        
        return json.load(f)
    
def update_tags(new_tags: dict[str, list[str]]) -> None:
    """first we will have to check what tags that already exist get new value appended.
    next we can check for new tags and add them to the dict."""

    existing_tags = load_tags()
    
    for tag, files in new_tags.items():
        if tag in existing_tags:
            existing_tags[tag].extend(files)
        else:
            existing_tags[tag] = files
    TAGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TAGS_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_tags, f, indent=2)