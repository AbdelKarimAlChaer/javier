import llm
import writer
import tag_manager
from rich.console import Console

console = Console()

def run(user_input: str) -> bool:
    try:
     
        response = llm.generate(user_input, list(tag_manager.load_tags().keys()))
        writer.save(response)
        return True
    except ConnectionError as e:
        console.print(f"✗ {e}", style="bold red")
        return False