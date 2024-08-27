#!/usr/bin/env python3
"""
Contains:
    Module-level
    ============
    app - A simple flask application serving a single route
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """Handles the root (/) route"""
    return render_template("0-index.html")

if __name__ == "__main__":
    app.run()
