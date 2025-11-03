import streamlit as st
import json
import random
import requests
from time import sleep

st.set_page_config(page_title="Magic Deck Randomizer", layout="wide")

# --- Load / Save JSON --- #
def load_players(file):
    try:
        return json.load(file)
    except Exception as e:
        st.error(f"Error loading JSON: {e}")
        return {}

def save_players(players, file_path="players.json"):
    with open(file_path, "w") as f:
        json.dump(players, f, indent=2)
    st.success(f"Players saved to {file_path}")

# --- Scryfall Image Fetching (fuzzy) --- #
def get_card_image(card_name):
    """Get the image URL for a Magic card using fuzzy search."""
    url = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("image_uris", {}).get("normal")
    except Exception:
        return None

# --- Sidebar Inputs --- #
st.sidebar.header("Player Setup")
num_players = st.sidebar.number_input("Number of Players", min_value=2, max_value=10, value=4, step=1)

players = {}

# Load from JSON if uploaded
json_file = st.sidebar.file_uploader("Upload players JSON", type="json")
if json_file:
    loaded_players = load_players(json_file)
    if loaded_players:
        players = loaded_players
        st.sidebar.success("Players loaded from JSON!")

# Enter players manually with reordering simulation
st.sidebar.subheader("Enter Player Names and Decks")
for i in range(num_players):
    name = st.sidebar.text_input(f"Player {i+1} Name", key=f"name_{i}")
    # Deck inputs
    deck1 = st.sidebar.text_input(f"Deck 1 for {name}", key=f"deck1_{i}")
    deck2 = st.sidebar.text_input(f"Deck 2 for {name}", key=f"deck2_{i}")
    deck3 = st.sidebar.text_input(f"Deck 3 for {name}", key=f"deck3_{i}")
    decks = [d for d in [deck1, deck2, deck3] if d]
    # Simulate drag-and-drop reorder with multiselect
    if decks:
        decks = st.sidebar.multiselect(f"Reorder {name}'s decks (drag to reorder)", options=decks, default=decks, key=f"reorder_{i}")
    if name and decks:
        players[name] = decks

# Save players option
if st.sidebar.button("Save Players to JSON"):
    save_players(players)

# --- Random Assignment --- #
st.header("Random Deck Assignment")

def assign_decks(players_dict):
    names = list(players_dict.keys())
    shuffled = names[:]
    while True:
        random.shuffle(shuffled)
        if all(a != b for a, b in zip(names, shuffled)):
            break
    assignment = {}
    for giver, receiver in zip(names, shuffled):
        deck = random.choice(players_dict[receiver])
        assignment[giver] = (receiver, deck)
    return assignment

# Simulated animated "drawing from the hat"
def draw_animation(giver, receiver, deck):
    st.subheader(f"{giver} is drawing a deck from {receiver}...")
    placeholder = st.empty()
    for _ in range(3):
        placeholder.text(f"{giver} is drawing... 🎴")
        sleep(0.3)
        placeholder.text(f"{giver} is drawing... ✨")
        sleep(0.3)
    placeholder.text(f"{giver} got {deck}!")
    img_url = get_card_image(deck)
    if img_url:
        st.image(img_url, width=200, caption=deck, output_format="PNG")
    else:
        st.info(f"No image found for '{deck}'. Showing closest match if available.")

if st.button("Roll Decks"):
    if len(players) < 2:
        st.warning("Enter at least 2 players to roll.")
    else:
        assignments = assign_decks(players)
        for giver, (receiver, deck) in assignments.items():
            draw_animation(giver, receiver, deck)

# Optional reroll
if st.button("Reroll"):
    if len(players) < 2:
        st.warning("Enter at least 2 players to reroll.")
    else:
        assignments = assign_decks(players)
        for giver, (receiver, deck) in assignments.items():
            draw_animation(giver, receiver, deck)
