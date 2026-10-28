
import pytest

from src.matcher import calculate_match, extract_skills


def test_extract_skills():
    text = "I use Python, SQL, Git and Machine Learning."

    skills = extract_skills(text)

    assert "python" in skills
    assert "sql" in skills
    assert "git" in skills
    assert "machine learning" in skills


def test_matching_skills():
    resume = "I have experience with Python, SQL and Git."
    job = "Required skills: Python, SQL, Git and AWS."

    results = calculate_match(resume, job)

    assert "python" in results["matched_skills"]
    assert "sql" in results["matched_skills"]
    assert "git" in results["matched_skills"]
    assert "aws" in results["missing_skills"]


def test_empty_resume_raises_error():
    with pytest.raises(ValueError):
        calculate_match(
            "",
            "Python developer with SQL skills",
        )


def test_empty_job_description_raises_error():
    with pytest.raises(ValueError):
        calculate_match(
            "Python developer with SQL skills",
            "",
        )


def test_score_is_in_range():
    results = calculate_match(
        "Python, SQL, Git and machine learning",
        "Python, SQL, Git and machine learning required",
    )

    assert 0 <= results["match_score"] <= 100
