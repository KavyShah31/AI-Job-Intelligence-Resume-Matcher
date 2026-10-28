
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS = [
    "python",
    "sql",
    "mysql",
    "sqlite",
    "postgresql",
    "pandas",
    "numpy",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data analysis",
    "data visualization",
    "matplotlib",
    "tensorflow",
    "pytorch",
    "nlp",
    "natural language processing",
    "generative ai",
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
        vectors = vectorizer.fit_transform(
            [resume_text, job_description]
        )

        return float(
            cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        )

    except ValueError:
        return 0.0


def _semantic_similarity(resume_text, job_description):
    """Use sentence-transformers embeddings if installed."""
    try:
        from sentence_transformers import SentenceTransformer

        # Load the lightweight model only when this function is called.
        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        embeddings = model.encode(
            [resume_text, job_description],
            normalize_embeddings=True,
        )

        score = float(np.dot(embeddings[0], embeddings[1]))

        return max(0.0, min(1.0, score)), "Sentence Transformers"

    except (ImportError, ModuleNotFoundError):
        return _tfidf_similarity(
            resume_text, job_description
        ), "TF-IDF fallback"

    except Exception:
        # Includes model download/network errors.
        return _tfidf_similarity(
            resume_text, job_description
        ), "TF-IDF fallback"


def calculate_match(resume_text, job_description):
    """
    Compare a resume with a job description.

    Returns match score, similarity, skills, and skill-gap analysis.
    """
    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    similarity, method = _semantic_similarity(
        resume_text, job_description
    )

    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    matched_skills = sorted(resume_skills & job_skills)
    missing_skills = sorted(job_skills - resume_skills)

    if job_skills:
        skill_score = len(matched_skills) / len(job_skills)
    else:
        skill_score = 0.0

    overall_score = (
        (0.60 * similarity) + (0.40 * skill_score)
    ) * 100

    return {
        "match_score": round(overall_score, 2),
        "text_similarity": round(similarity * 100, 2),
        "skill_match_score": round(skill_score * 100, 2),
        "matching_method": method,
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }
