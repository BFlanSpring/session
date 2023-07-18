
from flask import Flask, render_template, request, redirect, url_for, flash, session
from surveys import Question, Survey, surveys, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_ENABLED'] = False


@app.route('/')
def start():
    session['responses'] = []
    return redirect('/survey')

@app.route('/survey')
def survey():
    survey = surveys['satisfaction']

    # Initialize the responses list with None values for each question
    session['responses'] = [None] * len(survey.questions)

    return render_template('start.html', survey=survey)


@app.route('/questions/<int:question_index>', methods=['GET', 'POST'])
def question(question_index):
    survey = surveys['satisfaction']
    questions = survey.questions
    num_questions = len(questions)

    if question_index >= num_questions:
        return redirect('/thank-you')

    session['current_question_index'] = question_index
    current_question_index = session.get('current_question_index', 0)

    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer:
            session['responses'][current_question_index] = answer
            current_question_index += 1
            session['current_question_index'] = current_question_index

            if current_question_index == num_questions:
                return redirect('/thank-you')
        else:
            flash('Please select an answer.', 'error')

    # Ensure the user cannot access a question out of order
    if question_index != current_question_index:
        return redirect(url_for('question', question_index=current_question_index))

    question = questions[current_question_index]

    return render_template('question.html', question=question)




@app.route('/answer', methods=['POST'])
def answer():
    answer = request.form.get('answer')
    if answer:
        session['responses'][session['current_question_index']] = answer
        session['current_question_index'] += 1

        if session['current_question_index'] == len(surveys['satisfaction'].questions):
            return redirect('/thank-you')
    else:
        flash('Please select an answer.', 'error')

    return redirect(url_for('question', question_index=session['current_question_index']))


@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')
