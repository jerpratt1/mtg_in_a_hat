import random
import json
import os

SAVE_FILE = "players.json"

def assign_decks(players_with_decks):
    players = list(players_with_decks.keys())

    # Create a random derangement (no one gets themselves, no repeats)
    while True:
        assigned = players.copy()
        random.shuffle(assigned)
        if all(p != a for p, a in zip(players, assigned)):
            break

    results = {}
    for player, assigned_player in zip(players, assigned):
        chosen_deck = random.choice(players_with_decks[assigned_player])
        results[player] = {
            "assigned_player": assigned_player,
            "assigned_deck": chosen_deck
        }
    return results


def print_assignments(assignments):
    print("\nRandom Deck Assignments:")
    for player, info in assignments.items():
        print(f"  {player} gets {info['assigned_player']}'s '{info['assigned_deck']}' deck")
    print()


def get_player_info():
    print("Enter player names and their 3 decks")
    print("(Press Enter after each name and deck)\n")

    players_with_decks = {}
    while True:
        try:
            num_players = int(input("How many players? (e.g. 4): "))
            if num_players < 2:
                print("You need at least 2 players.")
                continue
            break
        except ValueError:
            print("Please enter a number.")

    for i in range(num_players):
        name = input(f"\nPlayer {i + 1} name: ").strip()
        if not name:
            name = f"Player{i + 1}"

        decks = []
        for j in range(3):
            deck_name = input(f"  Deck {j + 1} name for {name}: ").strip()
            if not deck_name:
                deck_name = f"Deck{j + 1}"
            decks.append(deck_name)
        players_with_decks[name] = decks
    return players_with_decks


def save_players(players_with_decks):
    with open(SAVE_FILE, "w") as f:
        json.dump(players_with_decks, f, indent=2)
    print(f"\nPlayer data saved to '{SAVE_FILE}'.")


def load_players():
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        print(f"\nLoaded players from '{SAVE_FILE}'.")
        if isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
            return data
        else:
            print("Invalid data format in save file.")
            return None
    except Exception as e:
        print(f"Could not load '{SAVE_FILE}': {e}")
        return None


def edit_players(players_with_decks):
    while True:
        print("\nPlayer Editing Menu:")
        print("1. Edit a player")
        print("2. Add a new player")
        print("3. Remove a player")
        print("4. Done editing")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("\nPlayers:")
            for idx, name in enumerate(players_with_decks.keys(), start=1):
                print(f"  {idx}. {name}")
            sel = input("Select player number to edit: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(players_with_decks):
                sel_idx = int(sel) - 1
                player_name = list(players_with_decks.keys())[sel_idx]

                new_name = input(f"Enter new name for {player_name} (or press Enter to keep): ").strip()
                if new_name:
                    players_with_decks[new_name] = players_with_decks.pop(player_name)
                    player_name = new_name

                print(f"Editing decks for {player_name}:")
                for i in range(3):
                    new_deck = input(f"  Deck {i+1} name (current: {players_with_decks[player_name][i]}): ").strip()
                    if new_deck:
                        players_with_decks[player_name][i] = new_deck
            else:
                print("Invalid selection.")

        elif choice == "2":
            name = input("New player name: ").strip()
            if not name:
                name = f"Player{len(players_with_decks)+1}"
            decks = []
            for i in range(3):
                deck_name = input(f"  Deck {i+1} name for {name}: ").strip()
                if not deck_name:
                    deck_name = f"Deck{i+1}"
                decks.append(deck_name)
            players_with_decks[name] = decks

        elif choice == "3":
            print("\nPlayers:")
            for idx, name in enumerate(players_with_decks.keys(), start=1):
                print(f"  {idx}. {name}")
            sel = input("Select player number to remove: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(players_with_decks):
                sel_idx = int(sel) - 1
                player_name = list(players_with_decks.keys())[sel_idx]
                del players_with_decks[player_name]
                print(f"{player_name} removed.")
            else:
                print("Invalid selection.")

        elif choice == "4":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    print("Magic Deck Randomizer")
    print("----------------------")

    players_with_decks = None

    # Optionally load existing players
    if os.path.exists(SAVE_FILE):
        choice = input(f"Load players from '{SAVE_FILE}'? (y/n): ").strip().lower()
        if choice in ("y", "yes"):
            players_with_decks = load_players()
            if players_with_decks:
                choice = input("Do you want to edit the loaded players? (y/n): ").strip().lower()
                if choice in ("y", "yes"):
                    edit_players(players_with_decks)

    # If not loaded, get new players
    if not players_with_decks:
        players_with_decks = get_player_info()

    # Show loaded players
    print("\nPlayers loaded:")
    for name, decks in players_with_decks.items():
        print(f"  {name}: {', '.join(decks)}")

    # Main reroll loop
    while True:
        assignments = assign_decks(players_with_decks)
        print_assignments(assignments)

        choice = input("Reroll? (y/n): ").strip().lower()
        if choice not in ("y", "yes"):
            break

    # Ask if we want to save the current players to file
    choice = input("\nDo you want to save these players to 'players.json'? (y/n): ").strip().lower()
    if choice in ("y", "yes"):
        save_players(players_with_decks)

    print("Good luck and have fun!")
    input("Press Enter to exit...")
