import typer
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer()
console = Console()

BASE_URL = "http://localhost:8000"


@app.command()
def add(text: str):
    """Add a new memory."""

    response = requests.post(f"{BASE_URL}/memory", json={"text": text})
    data = response.json()

    console.print(
        Panel(
            f"[bold green]Memory Stored Successfully[/bold green]\n\nID: {data['memory_id']}",
            title="Smart Memory System",
            border_style="green"
        )
    )


@app.command()
def search(query: str):
    """Search memories and get an AI answer."""

    response = requests.post(f"{BASE_URL}/query", json={"query": query})
    data = response.json()

    console.print("\n[bold cyan]Top Memories[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Rank")
    table.add_column("Memory")

    for i, memory in enumerate(data["top_memories"], 1):
        table.add_row(str(i), memory)

    console.print(table)

    console.print(
        Panel(
            data["answer"],
            title="AI Answer",
            border_style="blue"
        )
    )


if __name__ == "__main__":
    app()