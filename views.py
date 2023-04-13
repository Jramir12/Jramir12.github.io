#Author: Jonathan Ramirez
#Course Number: COSC 499
#Date Completed:4/7/2023
#Description: This program renders the HTML file and makes sure as we change things it will also change on our website
#Input: N/A
#output: Changes the website based on the changes done to the HTML
#things that need attention: being able to change the given Url

import importlib
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, app

views = Blueprint( __name__, "views")


#Jonathan Ramirez
#4/3/2023
# Renders the home page using the Url route provided 
#results: get website
@views.route("/")
def home():
    return render_template("index.html")

