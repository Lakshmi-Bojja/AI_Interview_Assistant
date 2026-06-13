from flask import Flask, render_template, request
import random
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

questions = {
    "Software Developer": [
        "Explain OOP concepts.",
        "What is inheritance?",
        "What is polymorphism?",
        "What is encapsulation?",
        "Difference between abstraction and encapsulation?",
        "What is a class?",
        "What is an object?",
        "What is method overriding?"
    ],

    "Python Developer": [
        "Difference between List and Tuple?",
        "What is a Python dictionary?",
        "Explain lambda functions.",
        "What are decorators?",
        "What is list comprehension?",
        "What is a generator?",
        "What is exception handling?",
        "What is PEP 8?"
    ],

    "Data Analyst": [
        "Difference between INNER JOIN and LEFT JOIN?",
        "What is normalization?",
        "What is a primary key?",
        "Explain GROUP BY.",
        "What is data cleaning?",
        "What is data visualization?",
        "What is SQL?",
        "What is a foreign key?"
    ],

    "Cloud Engineer": [
        "Benefits of cloud computing?",
        "What is scalability?",
        "What is load balancing?",
        "What is virtualization?",
        "Difference between public and private cloud?",
        "What is disaster recovery?",
        "What is SaaS?",
        "What is IaaS?"
    ],

    "AWS Engineer": [
        "What is Amazon EC2?",
        "What is S3?",
        "What is IAM?",
        "What is Auto Scaling?",
        "Difference between EC2 and Lambda?",
        "What is VPC?",
        "What is Route 53?",
        "What is CloudWatch?"
    ]
}


@app.route("/")
def home():
    return render_template(
        "index.html",
        question="",
        score="",
        feedback="",
        resume_score="",
        skills=[]
    )


@app.route("/upload_resume", methods=["POST"])
def upload_resume():

    file = request.files.get("resume")

    if not file:
        return "No file uploaded"

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(filepath)

    # Demo score and skills
    resume_score = "85%"

    skills = [
        "Python",
        "Flask",
        "SQL",
        "HTML",
        "CSS"
    ]

    return render_template(
        "index.html",
        resume_score=resume_score,
        skills=skills,
        question="",
        score="",
        feedback=""
    )


@app.route("/generate_question", methods=["POST"])
def generate_question():

    interview_type = request.form.get(
        "interview_type"
    )

    question = random.choice(
        questions.get(
            interview_type,
            ["Tell me about yourself."]
        )
    )

    return render_template(
        "index.html",
        question=question,
        score="",
        feedback="",
        resume_score="",
        skills=[]
    )


@app.route("/submit_answer", methods=["POST"])
def submit_answer():

    question = request.form.get(
        "question",
        ""
    )

    answer = request.form.get(
        "answer",
        ""
    ).strip().lower()

    no_answer_words = [
        "",
        "i don't know",
        "dont know",
        "don't know",
        "nothing",
        "no idea",
        "skip",
        "n/a",
        "-"
    ]

    if answer in no_answer_words:
        score = "0/10"
        feedback = "You did not answer the question."

    elif len(answer) >= 150:
        score = "10/10"
        feedback = "Excellent answer. Very detailed explanation."

    elif len(answer) >= 100:
        score = "9/10"
        feedback = "Very good answer with strong explanation."

    elif len(answer) >= 60:
        score = "8/10"
        feedback = "Good answer."

    elif len(answer) >= 30:
        score = "6/10"
        feedback = "Average answer. Add more details."

    elif len(answer) >= 10:
        score = "3/10"
        feedback = "Answer is too short."

    else:
        score = "1/10"
        feedback = "Very weak answer."

    return render_template(
        "index.html",
        question=question,
        score=score,
        feedback=feedback,
        resume_score="",
        skills=[]
    )


if __name__ == "__main__":
    app.run(debug=True)