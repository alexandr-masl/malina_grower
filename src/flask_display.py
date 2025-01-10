from flask import Flask, jsonify, render_template
import json
import os
from datetime import datetime

# Flask App
app = Flask(__name__)

# Path to the status file
status_file_path = os.path.join(os.path.dirname(__file__), "status.json")

# Route to display the main page
@app.route("/")
def index():
    return render_template("index.html")

# Route to provide JSON data for the table
@app.route("/api/shots")
def get_shots():
    try:
        with open(status_file_path, "r") as status_file:
            data = json.load(status_file)
            return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Status file not found"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
