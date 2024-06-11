from flask import Flask, render_template, request, url_for, redirect
import re, os
import csv
from functions import search_director
import json

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    global director_name    # Declare director name being searched as a global variable
    global results          # Declare search results as a global variable
    if request.method == 'POST':
        director_name = request.form.get("director-name")

        results = search_director(director_name)

        return redirect("/results")

    else:
        return render_template("index.html")


@app.route("/results", methods=['GET'])
def results_page():
    # global results

    return render_template("results.html", results=results)