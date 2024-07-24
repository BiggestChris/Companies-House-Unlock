from flask import Flask, render_template, request, url_for, redirect, session
import re, os
import csv
from functions import search_director, get_director_details, get_company_details
import json
from itertools import groupby
from operator import itemgetter
import calendar
from flask_session import Session

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    """
    session['director_name']    # Declare director name being searched as a global variable
    session['officers']
    session['officers_with_companies']
    """

    # director_details = []
    # company_details = []

    if request.method == 'POST':
        session['director_name'] = request.form.get("director-name")
        search_results = search_director(session['director_name'])
        session['officers'] = search_results['items'] if search_results and 'items' in search_results else []
        session['officers_with_companies'] = []

        for officer in session['officers']:
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
                session['officers_with_companies'].append(officer)

        return redirect("/results")

    else:
        return render_template("index.html")


@app.route("/results", methods=['GET'])
def results_page():
    # global results
    
    sorted_officers = {}
    unknown = []

    for officer in session['officers_with_companies']:
        try:
            DoB = str(calendar.month_name[officer['date_of_birth']['month']][0:3]) + "-" + str(officer['date_of_birth']['year'])

            # print(DoB)
            if DoB in sorted_officers:
                sorted_officers[DoB].append(officer)
            else:
                sorted_officers[DoB] = []
                sorted_officers[DoB].append(officer)
        except KeyError:
                unknown.append(officer)

    sorted_officers["Unknown"] = unknown
    print("Search ran successfully", flush=True)

    return render_template("results.html", director_name=session['director_name'], sorted_officers=sorted_officers)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)