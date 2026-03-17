import typer
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

app = typer.Typer(help="Smart Memory System CLI")
console = Console()

BASE_URL = "http://localhost:8000"


# ---------- Helper Functions ---------- #

def handle_api_error(response):
    if response.status_code != 200:
        console.print(
            Panel(
                f"[bold red]API Error[/bold red]\n\n{response.text}",
                border_style="red"
            )
        )
        raise typer.Exit()


def safe_json(response):
    try:
        return response.json()
    except Exception:
        console.print(
            Panel(
                "[bold red]Invalid JSON response from API[/bold red]",
                border_style="red"
            )
        )
        raise typer.Exit()


# ---------- Commands ---------- #

@app.command()
def add(text: str):
    """Add a new memory"""

    response = requests.post(f"{BASE_URL}/memory", json={"text": text})
    handle_api_error(response)

    data = safe_json(response)

    console.print(
        Panel(
            f"[bold green]Memory Stored[/bold green]\n\n"
            f"[cyan]ID:[/cyan] {data.get('memory_id')}\n"
            f"[cyan]Importance:[/cyan] {round(data.get('importance', 0), 2)}",
            title="Smart Memory System",
            border_style="green",
        )
    )


@app.command()
def search(query: str):
    """Search memories and get an AI answer"""

    response = requests.post(f"{BASE_URL}/query", json={"query": query})
    handle_api_error(response)

    data = safe_json(response)

    # Case 1 — Only answer (no memories returned)
    if "top_memories" not in data:
        console.print(
            Panel(
                data.get("answer", "No answer available"),
                title="[bold blue]AI Answer[/bold blue]",
                border_style="blue"
            )
        )
        return

    # Case 2 — No memories
    if not data["top_memories"]:
        console.print(
            Panel(
                "[yellow]No memory found[/yellow]",
                title="Search Result",
                border_style="yellow"
            )
        )

        console.print(
            Panel(
                data.get("answer", "No answer available"),
                title="[bold blue]AI Answer[/bold blue]",
                border_style="blue"
            )
        )
        return

    # Case 3 — Normal flow (memories + answer)
    table = Table(
        title="Top Memories",
        header_style="bold magenta",
        box=box.ROUNDED
    )

    table.add_column("Rank", style="cyan", justify="center")
    table.add_column("Memory", style="white")

    for i, memory in enumerate(data["top_memories"], 1):
        table.add_row(str(i), memory)

    console.print(table)

    console.print(
        Panel(
            data.get("answer", "No answer generated"),
            title="[bold blue]AI Answer[/bold blue]",
            border_style="blue"
        )
    )


@app.command()
def status(memory_id: str):
    """Check memory state and strength"""

    response = requests.get(f"{BASE_URL}/memory/{memory_id}")
    handle_api_error(response)

    data = safe_json(response)

    console.print(
        Panel(
            f"[bold]Text:[/bold] {data.get('text')}\n\n"
            f"[cyan]State:[/cyan] {data.get('state')}\n"
            f"[cyan]Strength:[/cyan] {round(data.get('strength', 0), 2)}\n"
            f"[cyan]Importance:[/cyan] {round(data.get('importance', 0), 2)}\n"
            f"[cyan]Access Count:[/cyan] {data.get('access_count')}\n"
            f"[cyan]Last Accessed:[/cyan] {data.get('last_accessed')}",
            title="Memory Status",
            border_style="yellow"
        )
    )


# ---------- Entry ---------- #

if __name__ == "__main__":
    app()