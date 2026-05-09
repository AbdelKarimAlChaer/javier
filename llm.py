
import requests
import config
import tag_manager



def generate(prompt: str, tags: list[str]) -> str:
    
    SYSTEM_PROMPT = f"""You are Javier, an assistant that structures thoughts into markdown notes.

RULES:
- Do NOT invent anything
- ONLY rephrase what the user has written
- No advice, no explanations, no general knowledge
- Return ONLY the markdown, nothing else
- Match the tags you create against this list of existing categories and only add new ones if necessary: {tags}

# Title (derived from the user's thought)

**Tags:** [2-4 tags with #]

## Thought
[The user's thought, lightly structured but NOT expanded]

"""

    full_prompt =f"{SYSTEM_PROMPT}\n\nUser-Thought:{prompt}"
    payload = {
        "model": config.MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {
        "temperature": config.TEMPERATURE,
        "num_predict": config.MAX_TOKENS
        }
    }
    try:
        response = requests.post(config.OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Fehler bei der Verbindung zum LLM: {e}")