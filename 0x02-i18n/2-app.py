#!/usr/bin/env python3
"""
Contains:
    Module-level
    ============
    app - A flask application
    babel - A Babel instance to support multiple languages in our app
"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Configuration for the flask application"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


def get_locale():
    """
    Selects most appropriate locale from the supported
    based on the request's Accept-Languages header value
    """
    return request.accept_languages.best_match(app.config["LANGUAGES"])


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app, locale_selector=get_locale)


@app.route("/")
def index():
    """Handles the root (/) route"""
    return render_template("1-index.html")


if __name__ == "__main__":
    app.run()
