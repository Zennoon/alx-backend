#!/usr/bin/env python3
"""
Contains:
    Module-level
    ============
    app - A flask application
    babel - A Babel instance to support multiple languages in our app
"""
from flask import Flask, g, render_template, request
from flask_babel import Babel
from typing import Dict, Union


class Config:
    """Configuration for the flask application"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """
    Selects most appropriate locale from the supported
    based on the request's Accept-Languages header value
    """
    url_locale = request.args.get("locale")
    if url_locale and url_locale in app.config["LANGUAGES"]:
        return url_locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


def get_user() -> Union[Dict, None]:
    """Retrieves the user logging in"""
    user_id = request.args.get("login_as")
    if user_id:
        try:
            user_id = int(user_id)
        except ValueError:
            return None
        return users[user_id]
    return None


@app.before_request
def before_request():
    g.user = get_user()


@app.route("/", strict_slashes=False)
def index() -> str:
    """Handles the root (/) route"""
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run()
