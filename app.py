import json
import os
import random


def load_quotes(filename="quotes.json"):
    """Load quotes from a JSON file."""
    # Find the quotes file in the same directory as this script if needed
    filepath = filename
    if not os.path.exists(filepath):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, filename)

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            quotes = json.load(file)
            if not isinstance(quotes, list) or len(quotes) == 0:
                print("Error: The quotes file does not contain a list of quotes.")
                return None
            return quotes
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'. Please make sure the file exists.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to read '{filename}'. Please check that it contains valid JSON.")
        return None
    except Exception as error:
        print(f"Error reading '{filename}': {error}")
        return None


def show_title():
    """Display the application title banner."""
    print("================================")
    print("       RANDOM QUOTE GENERATOR")
    print("================================")


def show_help():
    """Display available commands."""
    print("q - Get a random quote")
    print("h - Show help")
    print("x - Exit")


def display_random_quote(quotes):
    """Pick and display a random quote from the list."""
    selected_quote = random.choice(quotes)
    print(f'"{selected_quote["quote"]}"')
    print(f'— {selected_quote["author"]}')


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
            print("\nGoodbye!")
            break

        if command == "q":
            display_random_quote(quotes)
        elif command == "h":
            show_help()
        elif command == "x":
            print("Goodbye!")
            break
        elif command == "":
            continue
        else:
            print("Invalid command. Type 'h' to show help.")


if __name__ == "__main__":
    main()
