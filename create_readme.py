# Python script to create quick_start_readme.txt

readme_text = """Magic Deck Randomizer - Quick Start

Quick Setup
1. Install Python 3.10+
2. Install Streamlit
   Run the following commands in your terminal or PowerShell:
   python -m pip install --upgrade pip
   python -m pip install streamlit

3. Run the app
   python -m streamlit run deck_in_a_hat_streamlit.py
   The app will open in your default web browser.

Quick Usage
- Edit player names and decks in the interface.
- Optionally, upload a 'players.json' file to load players.
- Click Assign Decks to randomly assign decks.
- Click Reroll Assignment for a new random assignment.
- Click Save current players to JSON to export the current setup.

JSON Format
Example 'players.json' format:
{
  "Alice": ["Deck A1", "Deck A2", "Deck A3"],
  "Bob": ["Deck B1", "Deck B2", "Deck B3"],
  "Charlie": ["Deck C1", "Deck C2", "Deck C3"],
  "Dana": ["Deck D1", "Deck D2", "Deck D3"]
}
"""

# Save to a text file
with open("quick_start_readme.txt", "w") as file:
    file.write(readme_text)

print("quick_start_readme.txt created successfully!")
