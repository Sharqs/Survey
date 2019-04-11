from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys
import pdb 


app=Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)


responses = []

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
SURVEY = surveys.satisfaction_survey

@app.route("/home")
def home():
    session["responses"] = []
  
    instructions = surveys.satisfaction_survey.instructions
    title = surveys.satisfaction_survey.title
    return render_template('/home.html', instructions=instructions, title=title)

# old code
# @app.route("/redirect", methods=["POST"])
# def redirect_to_first_question():
#   session["responses"] = []
#   return redirect('question/0')

@app.route(f"/questions/{len(SURVEY.questions)}")
def ending_page():
  """ Reached when you hit the last survey question """
  if len(session["responses"]) == len(SURVEY.questions):
    flash("Survey completed!")
    flash("Thanks for your DATA :) ")
    return redirect("/home")
  else:
    flash("NO, YOU WILL GIVE US YOUR DATA")
    return redirect(f'/questions/{len(session["responses"])}')


@app.route("/questions/<int:question_number>")
def questions(question_number):
    
    if question_number > len(session["responses"]):
      flash("WE NEED ALL YOUR DATA")

      return redirect(f'/questions/{len(session["responses"])}')

    current_question = surveys.satisfaction_survey.questions[question_number]
    

    return render_template('/questions.html', question=current_question, question_number=question_number)

@app.route("/questions", methods=["POST"])
def routing():
    print("-" * 20)
    number = int([*request.form.keys()][0]) 
   
    responses = session["responses"]
    responses.append(request.form[str(number)])
    session["responses"] = responses

    print("This is what we have for session", session)
    print("Responses we've collected so far with sessions:", session["responses"])

    return redirect(f'/questions/{len(session["responses"])}')




#@app.route(f"questions/{len(surveys.questions)+1}")