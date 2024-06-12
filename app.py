from flask import Flask, render_template, request, url_for, redirect
import re, os
import csv
from functions import search_director, get_director_details, get_company_details
import json

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    global director_name    # Declare director name being searched as a global variable
    global officers
    global officers_with_companies

    # director_details = []
    # company_details = []

    if request.method == 'POST':
        director_name = request.form.get("director-name")
        search_results = search_director(director_name)
        officers = search_results['items'] if search_results and 'items' in search_results else []
        officers_with_companies = []

        for officer in officers:
            officer_id = officer['links']['self'].split('/')[2]
            director_details = get_director_details(officer_id)
            if director_details and 'items' in director_details:
                companies = []
                for appointment in director_details['items']:
                    company_number = appointment['appointed_to']['company_number']
                    company_detail = get_company_details(company_number)
                    if company_detail:
                        companies.append(company_detail)
                officer['companies'] = companies
                officers_with_companies.append(officer)

        return redirect("/results")

    else:
        return render_template("index.html")


@app.route("/results", methods=['GET'])
def results_page():
    # global results

    return render_template("results.html", director_name=director_name, officers=officers_with_companies)