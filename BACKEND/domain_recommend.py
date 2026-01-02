# DOMAIN RECOMMENDATION ENGINE (REALISTIC VERSION)

# Domain → Most common skills/keywords
DOMAIN_KEYWORDS = {
    "Artificial Intelligence": [
        "python", "machine learning", "ai", "deep learning", "pandas",
        "numpy", "tensorflow", "pytorch", "neural", "data analysis", "ml"
    ],
    "Web Development": [
        "html", "css", "javascript", "react", "node", "bootstrap",
        "frontend", "backend", "full stack", "web app", "express"
    ],
    "Cloud Computing": [
        "aws", "azure", "gcp", "docker", "kubernetes", "devops",
        "cloud", "terraform", "linux"
    ],
    "Cyber Security": [
        "security", "ethical hacking", "penetration testing",
        "cyber", "network security", "vulnerability", "malware"
    ],
    "Data Analyst": [
        "excel", "sql", "tableau", "power bi", "data cleaning",
        "visualization", "analytics", "statistics", "python"
    ],
    "Mobile App Development": [
        "android", "flutter", "kotlin", "java", "react native",
        "mobile app", "ios"
    ]
}

# Interest categories → Domain alignment
INTEREST_MAP = {
    "designing": ["Web Development", "Mobile App Development"],
    "creative": ["Web Development"],
    "uiux": ["Web Development", "Mobile App Development"],
    "developing": ["Web Development", "Mobile App Development", "Artificial Intelligence"],
    "apps": ["Mobile App Development"],
    "coding": ["Web Development", "Artificial Intelligence", "Data Analyst"],
    "data": ["Data Analyst", "Artificial Intelligence"],
    "math": ["Artificial Intelligence", "Data Analyst"],
    "problem": ["Artificial Intelligence"],
    "security": ["Cyber Security"],
    "ethical": ["Cyber Security"],
    "games": ["Artificial Intelligence", "Mobile App Development"],
    "mobile": ["Mobile App Development"],
    "aitools": ["Artificial Intelligence"]
}


def get_resume_matched_skills(text, domain):
    """Return list of skills found in resume for a domain."""
    matched = []
    for skill in DOMAIN_KEYWORDS[domain]:
        if skill.lower() in text:
            matched.append(skill)
    return matched


def get_interest_matches(interests_list, domain):
    """Return interests that align with the domain."""
    matched = []
    for interest in interests_list:
        if interest in INTEREST_MAP:
            if domain in INTEREST_MAP[interest]:
                matched.append(interest)
    return matched


def predict_domain(text, interests_str):
    """
    Main intelligent prediction:
    ✔ Converts interests string → list
    ✔ Scores all domains based on resume skills + interests
    ✔ Returns: domain, matched resume skills, matched interests
    """

    # Convert "coding,math,apps" → ["coding","math","apps"]
    interests_list = [i.strip() for i in interests_str.split(",") if i.strip()]

    best_domain = None
    best_score = -1
    best_resume_skills = []
    best_interest_hits = []

    for domain in DOMAIN_KEYWORDS:

        resume_matches = get_resume_matched_skills(text, domain)
        interest_matches = get_interest_matches(interests_list, domain)

        resume_score = len(resume_matches)
        interest_score = len(interest_matches)

        # Weighted scoring
        total_score = (resume_score * 0.7) + (interest_score * 0.3)

        if total_score > best_score:
            best_score = total_score
            best_domain = domain
            best_resume_skills = resume_matches
            best_interest_hits = interest_matches

    # Final output
    return best_domain, best_resume_skills, best_interest_hits
