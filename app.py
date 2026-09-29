import json
import os
import random
import pyfiglet
from rich.console import Console
from rich.panel import Panel

console = Console()


def load_quotes(filename="quotes.json"):
    """Load quotes from a JSON file."""
    filepath = filename
    if not os.path.exists(filepath):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, filename)

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            quotes = json.load(file)
            if not isinstance(quotes, list) or len(quotes) == 0:
                console.print("[bold red]Error:[/bold red] The quotes file does not contain a list of quotes.")
                return None
            return quotes
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] Could not find '{filename}'. Please make sure the file exists.")
        return None
    except json.JSONDecodeError:
        console.print(f"[bold red]Error:[/bold red] Failed to read '{filename}'. Please check that it contains valid JSON.")
        return None
    except Exception as error:
        console.print(f"[bold red]Error reading '{filename}':[/bold red] {error}")
        return None


def show_title():
    """Display the ASCII-art application title banner."""
    ascii_banner = pyfiglet.figlet_format("Quote Gen", font="standard")
    console.print(f"[bold cyan]{ascii_banner}[/bold cyan]")
    console.print("[bold yellow]================================[/bold yellow]")
    console.print("[bold yellow]       RANDOM QUOTE GENERATOR    [/bold yellow]")
    console.print("[bold yellow]================================[/bold yellow]")


def show_help():
    """Display available commands."""
    console.print("[bold green]q[/bold green] - Get a random quote")
    console.print("[bold green]h[/bold green] - Show help")
    console.print("[bold green]x[/bold green] - Exit")


def display_random_quote(quotes):
    """Pick and display a random quote from the list."""
    selected_quote = random.choice(quotes)
    quote_text = selected_quote["quote"]
    author = selected_quote["author"]
    quote_card = f'"{quote_text}"\n\n[italic cyan]— {author}[/italic cyan]'
    console.print(Panel(quote_card, title="Random Quote", border_style="cyan", expand=False))


def main():
    quotes = load_quotes()
    if quotes is None:
        return

    show_title()
    show_help()

    while True:
        try:
            command = input("> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold yellow]Goodbye![/bold yellow]")
            break

        if command == "q":
            display_random_quote(quotes)
        elif command == "h":
            show_help()
        elif command == "x":
            console.print("[bold yellow]Goodbye![/bold yellow]")
            break
        elif command == "":
            continue
        else:
            console.print("[red]Invalid command.[/red] Type '[bold green]h[/bold green]' to show help.")


if __name__ == "__main__":
    main()
