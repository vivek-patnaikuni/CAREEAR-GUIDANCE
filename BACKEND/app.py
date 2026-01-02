from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from domain_recommend import predict_domain
from skill_match import calculate_skill_match
from resume_improve import generate_resume_suggestions
from utils import extract_text_from_pdf

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# HOME ROUTE
@app.route("/", methods=["GET"])
def home():
    return "Career Guidance Backend is Running Successfully!", 200


# 1️ DOMAIN RECOMMENDATION ROUTE
@app.route("/recommend_domain", methods=["POST"])
def recommend_domain():
    resume = request.files.get("resume")
    interests = request.form.get("interests", "")

    if not resume:
        return jsonify({"error": "Resume not uploaded"}), 400

    # Save resume file
    path = os.path.join(UPLOAD_FOLDER, resume.filename)
    resume.save(path)

    # Extract PDF text
    text = extract_text_from_pdf(path)

    # Predict domain + extract matched skills + interests
    domain, skill_keywords, interests_list = predict_domain(text, interests)

    return jsonify({
        "domain": domain,
        "skill_keywords": skill_keywords,
        "interests_list": interests_list
    })


# 2️ SKILL MATCH ROUTE
@app.route("/skill_match", methods=["POST"])
def skill_match():
    resume = request.files.get("resume")
    selected_domain = request.form.get("domain", "")

    if not resume:
        return jsonify({"error": "Resume not uploaded"}), 400

    path = os.path.join(UPLOAD_FOLDER, resume.filename)
    resume.save(path)

    text = extract_text_from_pdf(path)

    percent, strengths, focus = calculate_skill_match(text, selected_domain)

    return jsonify({
        "percent": percent,
        "strengths": strengths,
        "focus": focus
    })


# 3️ RESUME IMPROVEMENT ROUTE

@app.route("/improve_resume", methods=["POST"])
def improve_resume():
    resume = request.files.get("resume")

    if not resume:
        return jsonify({"error": "Resume not uploaded"}), 400

    path = os.path.join(UPLOAD_FOLDER, resume.filename)
    resume.save(path)

    text = extract_text_from_pdf(path)

    suggestions = generate_resume_suggestions(text)

    return jsonify({
        "suggestions": suggestions
    })


# RUN LOCALLY

if __name__ == "__main__":
    app.run(debug=True)
