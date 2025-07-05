# job_matcher.py

def match_jobs(resume_text, top_k=5):
    # Predefined sample job roles with associated keywords
    sample_jobs = [
        {"title": "Software Developer", "keywords": ["python", "java", "api", "flask", "backend"]},
        {"title": "Data Scientist", "keywords": ["machine learning", "pandas", "numpy", "statistics", "data"]},
        {"title": "Frontend Engineer", "keywords": ["react", "html", "css", "javascript", "frontend"]},
        {"title": "Backend Developer", "keywords": ["django", "node", "express", "sql", "server"]},
        {"title": "DevOps Engineer", "keywords": ["docker", "aws", "ci/cd", "kubernetes", "infrastructure"]},
        {"title": "AI Engineer", "keywords": ["deep learning", "neural networks", "tensorflow", "vision"]},
    ]

    # Normalize resume text for keyword scanning
    resume_text_lower = resume_text.lower()
    matches = []

    for job in sample_jobs:
        match_score = sum(1 for kw in job["keywords"] if kw in resume_text_lower)
        matches.append((match_score, job["title"]))

    # Sort by match score and return top job titles
    matches.sort(reverse=True)
    return [title for score, title in matches if score > 0][:top_k]

