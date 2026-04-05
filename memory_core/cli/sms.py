import typer
import requests
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

app = typer.Typer(help="Smart Memory System CLI")
console = Console()

BASE_URL = "http://localhost:8000"

# 🔐 Supabase config (REPLACE THESE)
SUPABASE_URL = "https://zizfygdqcfcxhonawffk.supabase.co"
SUPABASE_API_KEY = "sb_publishable_jgFPwCRrMOF2ieiay3XU_Q_uAtVjSOg"

# 📁 Token storage
TOKEN_PATH = os.path.expanduser("~/.memoryfade_token")


# ---------- TOKEN HELPERS ---------- #

def save_token(token: str):
    with open(TOKEN_PATH, "w") as f:
        f.write(token)


def load_token():
    if not os.path.exists(TOKEN_PATH):
        console.print("[red]Not logged in. Run: login[/red]")
        raise typer.Exit()
    with open(TOKEN_PATH, "r") as f:
        return f.read().strip()


def get_headers():
    token = load_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


# ---------- ERROR HANDLING ---------- #

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


# ---------- AUTH COMMAND ---------- #

@app.command()
def login(email: str, password: str):
    """Login using Supabase"""

    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"

    headers = {
        "apikey": SUPABASE_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json={
        "email": email,
        "password": password
    })

    if response.status_code != 200:
        console.print(
            Panel(
                f"[bold red]Login Failed[/bold red]\n\n{response.text}",
                border_style="red"
            )
        )
        raise typer.Exit()

    data = response.json()
    token = data["access_token"]

    save_token(token)

    console.print(
        Panel(
            "[bold green]Login Successful[/bold green]",
            border_style="green"
        )
    )


# ---------- MEMORY COMMANDS ---------- #

@app.command()
def add(text: str):
    """Add a new memory"""

    response = requests.post(
        f"{BASE_URL}/memory",
        json={"text": text},
        headers=get_headers()
    )

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

    response = requests.post(
        f"{BASE_URL}/query",
        json={"query": query},
        headers=get_headers()
    )

    handle_api_error(response)
    data = safe_json(response)


    console.print(
        Panel(
            data.get("answer", "No answer available"),
            title="[bold blue]AI Answer[/bold blue]",
            border_style="blue"
        )
    )




@app.command()
def status(memory_id: str):
    """Check memory state and strength"""

    response = requests.get(
        f"{BASE_URL}/memory/{memory_id}",
        headers=get_headers()
    )

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

@app.command()
def decay(memory_id: str):
    """Manually trigger decay on a memory."""
    response = requests.post(f"{BASE_URL}/memory/{memory_id}/decay")
    data = response.json()
    console.print(
        Panel(
            f"[bold]Strength:[/bold] {data['strength']}\n"
            f"[bold]State:[/bold] {data['state']}",
            title="Decay Applied",
            border_style="red"
        )
    )

# ---------- ENTRY ---------- #

if __name__ == "__main__":
    app()