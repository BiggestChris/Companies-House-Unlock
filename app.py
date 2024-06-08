from flask import Flask, render_template, request, url_for, redirect
import re, os
import csv
from functions import get_survey_response, craft_question, export, init_questions
import json

app = Flask(__name__)


'''
Pseudo-code for final solution
1. Present Question 1 on the screen for user
2. 
    a. Read user's submitted answer and call ChatGPT API to read it
    b. Count 1 question asked on counter module
    c. Output question and question response 'somewhere'
3. ChatGPT API to craft another question based on response of user and internal rules applied
4. Present Question 2 on the screen for user
5. 
    a. Read user's submitted answer and call ChatGPT API to read it
    b. Count 2 questions asked on counter module
    c. Output question and question response 'somewhere'
6. ChatGPT API to craft another question based on response of user and internal rules applied
7. Present Question 3 on the screen for user
8. 
    a. Read user's submitted answer and call ChatGPT API to read it
    b. Count 3 questions asked on counter module
    c. Output question and question response 'somewhere'
'''

'''
More thoughts
1. Use Flask to delineate survey from survey parameters
2. Load up survey within JavaScript page, call ChatGPT API within JavaScript to dynamically run the survey on the page
3. Load survey results to other Flask page
'''

responses = [] # Initialise response list
max_question = 5 # Number of questions in survey
question_number = 1 # Initialise survey
survey_objective = ""
questions = init_questions(max_question) # Initialise question bank list


@app.route("/", methods=('GET', 'POST'))
def index():
    global max_question
    global survey_objective
    global questions
    global question_number
    global responses
    if request.method == 'POST':
        max_question = int(request.form.get("question-number"))
        survey_objective = request.form.get("survey-objective")
        questions = init_questions(max_question)
        questions[0] = request.form.get("first-question")
        question_number = 1
        responses = []

        return redirect("/survey")

    else:
        return render_template("index.html")


@app.route("/survey", methods=('GET', 'POST'))
def question_page():
    global question_number  # Declare question_number as global

    if request.method == 'POST':
        responses.append(get_survey_response())
        
        if question_number < max_question:
            question_number += 1
            return redirect("/survey")
        else:
            return redirect("/")
    
    else:
        if question_number > 1:
            questions[question_number - 1] = craft_question(questions, responses, max_question, survey_objective)
        question_text = questions[question_number - 1]

        return render_template("question-layout.html", question_number=question_number, question_text=question_text)


@app.route("/responses", methods=('GET', 'POST'))
def responses_page():
    if request.method == 'POST':
        global survey_objective
        export(questions, responses, survey_objective)
        
        return redirect("/")
    
    else:
        questions_json = json.dumps(questions)
        responses_json = json.dumps(responses)

        return render_template("responses.html", questions=questions, responses=responses,
                               questions_json=questions_json, responses_json=responses_json, survey_objective=survey_objective)