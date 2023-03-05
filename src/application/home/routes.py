"""
Routes file for '/home' url paths
"""

from flask import Blueprint, render_template, redirect, url_for

HOME = Blueprint("home", __name__)


@HOME.route("/")
def rediret_home():
    """
    Redirect user from '/' route to '/home' route

    """
    return redirect(url_for("home.homepage"))


@HOME.route("/home")
def homepage():
    """
    Main landing page of the application
    """
    return render_template("home/homepage.html", title="Home")
