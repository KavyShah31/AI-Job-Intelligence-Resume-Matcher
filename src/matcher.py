import re

import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = [
    "python",
    "sql",
    "mysql",
    "sqlite",
    "postgresql",
    "pandas"
    "numpy",
    "scikit-learn"
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data analysis",
    "matplotlib",
    "tensoreflow"
    "pytorch"
    "nlp",
    "natural language processing"
    "generative ai"
    "llm",
    "langchain",
    "streamlit",
    "flask",
    "fastapi",
    "django",
    "rest api",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "excel",
    "communication",
    "problem solving",
]

def extract_skills(text):
    """Extract skills from text using a predefined skill dictionary."""
    normalized = text.lower()
    found = []

    for skill in SKILLS:
        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(skill)
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, normalized):
            found.append(skill)

    return sorted(set(found))

def _tfidf_similarity(resume_text, job_description):
    """Fallback similarity when sentence-transformers is unavailable."""
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
    )

    try:
        vectors = vectorizer.fit_transfrom(
            [resume_text, job_description]
        )

        return float(
            cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        )

    except ValueError:
        return 0.0
    