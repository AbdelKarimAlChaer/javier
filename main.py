import pipeline
from rich.console import Console


def main()-> None:
    console = Console()
    console.print("Welcome to the LLM Pipeline!", style="bold green")
    user_input = input("Enter your prompt: ")
    if(pipeline.run(user_input)):
        console.print("Your notes have been saved!", style="bold blue")


