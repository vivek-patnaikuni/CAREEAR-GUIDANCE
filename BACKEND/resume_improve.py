# RESUME IMPROVEMENT AI ENGINE

ACTION_VERBS = [
    "built", "designed", "developed", "created", "led", "managed",
    "implemented", "optimized", "analyzed", "improved", "automated"
]

IMPORTANT_SECTIONS = [
    "education", "skills", "projects", "experience", "certification",
    "achievements", "internship"
]


def check_missing_sections(text):
    suggestions = []

    for section in IMPORTANT_SECTIONS:
        if section not in text:
            suggestions.append(f"Add a proper '{section.title()}' section.")

    return suggestions


def check_links(text):
    suggestions = []

    if "github" not in text:
        suggestions.append("Add your GitHub link to showcase your work.")

    if "linkedin" not in text:
        suggestions.append("Include your LinkedIn profile for recruiters.")

    return suggestions


def check_projects(text):
    suggestions = []

    if "project" not in text:
        suggestions.append("Add at least 1–2 academic or personal projects.")
    else:
        if "python" in text or "react" in text or "ml" in text:
            pass  # project looks good
        else:
            suggestions.append("Include tech stack/tools used in your projects (e.g., Python, React, SQL).")

    return suggestions


def check_metrics(text):
    suggestions = []

    # Searching for metrics like %, numbers, improved by X
    if "%" not in text and "increased" not in text and "reduced" not in text:
        suggestions.append("Add measurable results to your resume (e.g., improved accuracy by 15%).")

    return suggestions


def check_action_verbs(text):
    suggestions = []

    # Check if resume uses strong action verbs
    uses_verbs = any(verb in text for verb in ACTION_VERBS)

    if not uses_verbs:
        suggestions.append(
            "Start bullet points with strong action verbs (e.g., Developed, Designed, Implemented)."
        )

    return suggestions


def generate_resume_suggestions(text):
    """
    Returns a list of improvement suggestions based on:
    • Missing sections
    • Links (GitHub/LinkedIn)
    • Projects quality
    • Use of metrics
    • Action verbs
    • Overall completeness
    """

    suggestions = []

    # 1. Missing sections
    suggestions += check_missing_sections(text)

    # 2. GitHub / LinkedIn
    suggestions += check_links(text)

    # 3. Project analysis
    suggestions += check_projects(text)

    # 4. Metrics (%, numbers)
    suggestions += check_metrics(text)

    # 5. Action verbs
    suggestions += check_action_verbs(text)

    # Ensure at least 5 suggestions
    if len(suggestions) < 5:
        suggestions.append("Your resume looks good. Consider improving formatting for a more professional appearance.")

    # Filter duplicates
    final_suggestions = list(dict.fromkeys(suggestions))

    # Limit to 7 for clean UI
    return final_suggestions[:7]
