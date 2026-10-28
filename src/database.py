import json
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "analysis_history.db"


def get_connection():
    """Create a connection to the local SQLite database."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create the analysis history table if it doesn't exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_name TEXT NOT NULL,
                job_title TEXT NOT NULL,
                match_score REAL NOT NULL,
                matching_method TEXT NOT NULL,
                matched_skills TEXT NOT NULL,
                missing_skills TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_analysis(
    resume_name,
    job_title,
    results,
):
    """Save analysis results without storing the full resume text."""
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO analysis_history (
                resume_name,
                job_title,
                match_score,
                matching_method,
                matched_skills,
                missing_skills
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                resume_name,
                job_title,
                results["match_score"],
                results["matching_method"],
                json.dumps(results["matched_skills"]),
                json.dumps(results["missing_skills"]),
            ),
        )

        return cursor.lastrowid


def get_analysis_history(limit=50):
    """Return the most recent analyses."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM analysis_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def clear_analysis_history():
    """Delete saved analysis history."""
    with get_connection() as connection:
        connection.execute("DELETE FROM analysis_history")
