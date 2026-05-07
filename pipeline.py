import llm
import writer
from rich.console import Console

console = Console()

def run(user_input: str) -> bool:
    try:
        response = llm.generate(user_input)
        writer.save(response)
        return True
    except ConnectionError as e:
        console.print(f"✗ {e}", style="bold red")
        return False