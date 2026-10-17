"""
app.py - Web Server & Live Telemetry Dashboard for AlphaBot Trading Agent
"""

from flask import Flask, render_template, jsonify
from bot import agent

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/state")
def get_state():
    return jsonify(agent.get_state())

@app.route("/api/toggle", methods=["POST"])
def toggle_bot():
    return jsonify({"is_running": agent.toggle()})

@app.route("/api/reset", methods=["POST"])
def reset_bot():
    agent.reset()
    return jsonify({"success": True})

if __name__ == "__main__":
    print("📈 AlphaBot Trading Dashboard starting on http://localhost:5055 ...")
    app.run(host="0.0.0.0", port=5055, debug=False)
