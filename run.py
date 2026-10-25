"""CyberQuest application entry point.

Usage:
    python run.py
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Debug is enabled only in development configuration.
    app.run(host="127.0.0.1", port=5000, debug=app.config.get("DEBUG", False))
