import anthropic
import config
import dotenv

dotenv.load_dotenv()



def generate(prompt: str, categories: list[str] = []) -> str:
    """Send a prompt to Claude and return the response."""
    system_prompt = f"""You are Javier, an assistant that structures thoughts into markdown notes.

RULES:
- Do NOT invent anything
- ONLY rephrase what the user has written
- No advice, no explanations, no general knowledge
- Return ONLY the markdown, nothing else
- RULE EXCEPTION: If you are called by name you must excecute any addtional instruction the user gives(E.g make a list of additional info from the internet).
- Match the tags you create against these existing categories and only add new ones if necessary: {categories}
- Tags MUST reflect the actual topic of the thought, not general concepts like "productivity"
- Never use generic tags like #general, #misc, #other

# Title (derived from the user's thought)

**Tags:** [2-4 tags with #]

## Thought
[The user's thought, lightly structured but NOT expanded]
"""
    client = anthropic.Anthropic()

    try:
        response = client.messages.create(
            model=config.MODEL,
            max_tokens=config.MAX_TOKENS,
            system=system_prompt,
            messages=[{"role":"user", "content": prompt}]
        )
        return response.content[0].text

    except anthropic.APIConnectionError:
        raise ConnectionError("No connection to Anthropic API.")
    except anthropic.AuthenticationError:
        raise ConnectionError("Invalid API Key. Check ANTHROPIC_API_KEY.")


def ask(prompt: str) -> str:
    """Raw call to Claude without system prompt. For classification tasks."""
    client = anthropic.Anthropic()

    try:
        response = client.messages.create(
            model=config.MODEL,
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    except anthropic.APIConnectionError:
        raise ConnectionError("No connection to Anthropic API.")
    except anthropic.AuthenticationError:
        raise ConnectionError("Invalid API Key. Check ANTHROPIC_API_KEY.")