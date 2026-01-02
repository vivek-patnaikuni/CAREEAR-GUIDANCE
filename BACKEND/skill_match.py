# DOMAIN SKILL MATCH ENGINE

# Domain → Required Skills
DOMAIN_SKILLS = {
    "Artificial Intelligence": [
        "python", "machine learning", "deep learning", "data analysis",
        "numpy", "pandas", "tensorflow", "pytorch", "statistics"
    ],
    "Web Development": [
        "html", "css", "javascript", "react", "node",
        "express", "bootstrap", "frontend", "backend"
    ],
    "Cloud Computing": [
        "aws", "azure", "gcp", "docker", "kubernetes",
        "devops", "linux", "terraform"
    ],
    "Cyber Security": [
        "security", "ethical hacking", "penetration testing",
        "vulnerability", "network security", "cyber"
    ],
    "Data Analyst": [
        "python", "sql", "excel", "tableau",
        "power bi", "data cleaning", "visualization", "statistics"
    ],
    "Mobile App Development": [
        "android", "flutter", "kotlin", "java",
        "react native", "mobile app"
    ]
}


def calculate_skill_match(resume_text, domain):
    """
    Compares resume text with domain skills.
    Returns:
    - match percentage
    - strengths (skills present)
    - focus areas (skills missing)
    """

    if domain not in DOMAIN_SKILLS:
        return 0, [], []

    required_skills = DOMAIN_SKILLS[domain]
    resume_text = resume_text.lower()

    strengths = []
    focus = []

    # Check each skill
    for skill in required_skills:
        if skill.lower() in resume_text:
            strengths.append(skill)
        else:
            focus.append(skill)

    # Calculate percentage
    if len(required_skills) > 0:
        percent = round((len(strengths) / len(required_skills)) * 100)
    else:
        percent = 0

    # Limit to top 6 for clean UI
    return percent, strengths[:6], focus[:6]
