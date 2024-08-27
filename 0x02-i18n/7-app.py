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
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError


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
    """
    url_locale = request.args.get("locale")
    if url_locale and url_locale in app.config["LANGUAGES"]:
        return url_locale
    if g.user:
        user_locale = g.user.get("locale")
        if user_locale and user_locale in app.config["LANGUAGES"]:
            return user_locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone():
    """
    Selects most appropriate timezone
    """
    url_timezone = request.args.get("timezone")
    if url_timezone:
        try:
            _ = timezone(url_timezone)
            return url_timezone
        except UnknownTimeZoneError:
            pass
    if g.user:
        user_timezone = g.user.get("timezone")
        if user_timezone:
            try:
                _ = timezone(url_timezone)
                return user_timezone
            except UnknownTimeZoneError:
                pass
    return app.config["BABEL_DEFAULT_TIMEZONE"]


def get_user():
    """Retrieves the user logging in"""
    user_id_str = request.args.get("login_as")
    if user_id_str:
        try:
            user_id = int(user_id_str)
        except ValueError:
            return None
        if user_id in users.keys():
            return users[user_id]
    return None


@app.before_request
def before_request() -> None:
    """Configurations before every request"""
    g.user = get_user()


@app.route("/", strict_slashes=False)
def index() -> str:
    """Handles the root (/) route"""
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run()
