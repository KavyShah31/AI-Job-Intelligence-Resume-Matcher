
# AI Job Intelligence & Resume Matcher

A Python-based application that compares resumes with job descriptions,
identifies matching and missing skills, and stores analysis history.

## Features

- Extract text from PDF resumes
- Detect skills using a predefined skill dictionary
- Compare resume and job-description text
- Use Sentence Transformers embeddings when available
- Fall back to TF-IDF similarity when needed
- Calculate an approximate match score
- Identify matching skills and skill gaps
- Save analysis history in SQLite
- Run automated tests with pytest

## Tech Stack

- Python
- Streamlit
- Sentence Transformers
- Scikit-learn
- NumPy
- PyMuPDF
- SQLite
- Pytest

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the application:

```powershell
python -m streamlit run app.py
```

Run tests:

```powershell
python -m pytest -v
```

## Project Structure

- `app.py`: Streamlit dashboard
- `src/resume_parser.py`: PDF text extraction
- `src/matcher.py`: Similarity and skill-gap analysis
- `src/database.py`: SQLite history storage
- `tests/test_matcher.py`: Automated tests
- `data/`: Local database and optional datasets
- `reports/`: Optional evaluation reports

## Limitations

- Scanned PDF resumes require OCR, which is not included.
- Skills are detected using a predefined dictionary.
- Match scores are approximate and should not be treated as hiring decisions.
- Sentence Transformers may need an internet connection for the initial model download.

## Privacy

Use test resumes while developing. The local database stores analysis metadata,
including the resume filename and detected skills, but not the complete resume text.
Review privacy and data-retention requirements before using real candidate data.
