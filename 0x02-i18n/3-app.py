#!/usr/bin/env python3
"""
Contains:
    Module-level
    ============
    app - A flask application
    babel - A Babel instance to support multiple languages in our app
"""
from flask import Flask, render_template, request
from flask_babel import Babel, gettext
from typing import Any


class Config:
    """Configuration for the flask application"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> Any:
    """
    Selects most appropriate locale from the supported
    based on the request's Accept-Languages header value
    """
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index() -> Any:
    """Handles the root (/) route"""
    return render_template("3-index.html", 
                           home_title=gettext("home_title"), 
                           home_header=gettext("home_header"))


if __name__ == "__main__":
    app.run()
