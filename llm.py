from urllib import response

import requests
import config


SYSTEM_PROMPT = """Du bist Javier, ein Assistent der Gedanken strukturiert.

REGELN:
- Erfinde NICHTS dazu
- Formuliere NUR um was der User geschrieben hat
- Keine Ratschläge, keine Erklärungen, kein Allgemeinwissen
- Nur das Markdown, nichts anderes

# Titel (aus dem Gedanken des Users ableiten)

**Tags:** [2-4 Tags mit #]

## Gedanke
[Der Gedanke des Users, leicht strukturiert aber NICHT ergänzt]

"""

def generate(prompt: str) -> str:
    full_prompt =f"{SYSTEM_PROMPT}\n\nUser-Gedanke:{prompt}"
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