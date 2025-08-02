from flask import Flask, render_template, jsonify, request
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import random

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

# --- Built-in backup ghost data ---
backup_ghosts = [
    {
        "name": "Eleanor Whitestone",
        "era": "Victorian Era (1870s)",
        "backstory": "Once a governess in a grand London manor, Eleanor perished in a tragic fire. Her spirit wanders in search of the children she once cared for.",
        "message": "Mind the whispers in the corridors — they are my lullabies.",
        "remedy": "Place a porcelain doll in the attic to comfort her."
    },
    {
        "name": "Captain Silas Black",
        "era": "Golden Age of Piracy (1720s)",
        "backstory": "A feared pirate betrayed by his own crew. His ghost lingers near harbors, guarding his hidden treasure.",
        "message": "The sea remembers… and so do I.",
        "remedy": "Cast a silver coin into the ocean under a full moon."
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detect-ghost", methods=["POST"])
def detect_ghost():
    try:
        prompt = """
        You are a haunted investigation AI.
        Generate a fictional ghost profile with:
        - name
        - era (time period)
        - backstory
        - message
        - remedy to appease the ghost
        Format as pure JSON with keys:
        name, era, backstory, message, remedy
        """

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        if not response or not hasattr(response, "text") or not response.text:
            print("⚠ No response from Gemini — using backup ghost.")
            return jsonify(random.choice(backup_ghosts))

        text_output = response.text.strip()

        # Remove any markdown formatting if present
        if text_output.startswith("```json"):
            text_output = text_output.replace("```json", "").replace("```", "").strip()

        # Try parsing JSON
        try:
            ghost_data = json.loads(text_output)
        except json.JSONDecodeError:
            print("⚠ Gemini returned invalid JSON — using backup ghost.")
            return jsonify(random.choice(backup_ghosts))

        # Make sure all keys exist
        required_keys = ["name", "era", "backstory", "message", "remedy"]
        if not all(key in ghost_data for key in required_keys):
            print("⚠ Missing keys in Gemini response — using backup ghost.")
            return jsonify(random.choice(backup_ghosts))

        return jsonify(ghost_data)

    except Exception as e:
        print("⚠ ERROR:", e)
        return jsonify(random.choice(backup_ghosts))

if __name__ == "__main__":
    app.run(debug=True)
