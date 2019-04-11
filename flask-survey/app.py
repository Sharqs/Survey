from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
import surveys


app=Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

responses = []

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route("/home")
def home():
    instructions = surveys.satisfaction_survey.instructions
    title = surveys.satisfaction_survey.title
    return render_template('/home.html', instructions=instructions, title=title)


@app.route("/questions/<int:question_number>")
def questions(question_number):
    
    print("+++" * 100)
    print("rendering... ", question_number)
    current_question = surveys.satisfaction_survey.questions[question_number]
    
    next_question_number = question_number+1
    return render_template('/questions.html', question=current_question, question_number=next_question_number)

@app.route("/questions.html")
def routing(question_number):
    print("Hey I'm about redirect")
    return redirect(f'/questions/{question_number}')



#@app.route(f"questions/{len(surveys.questions)+1}")