import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@app.route("/")
def home():
    return render_template("landing.html")


@app.route("/email")
def email():
    return render_template("email.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/generate", methods=["POST"])
def generate_email():
    data = request.json

    name = data.get("name")
    recipient_name = data.get("recipientName")
    field_of_study = data.get("fieldOfStudy")
    school = data.get("school")
    purpose = data.get("purpose")
    tone = data.get("tone")

    prompt = f"""
    You are ColdCraft, an expert cold email writer for students.

    Write:
    1. A strong subject line
    2. A professional email body
    3. A short follow-up email

    Student Name: {name}
    Recipient Name: {recipient_name}
    Field of Study: {field_of_study}
    School/University/Campus: {school}
    Purpose: {purpose}
    Tone: {tone}

    You must return a clean email with proper formatting and no extra text and symbols.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return jsonify({"email": response.text})


if __name__ == "__main__":
    app.run(debug=True)
