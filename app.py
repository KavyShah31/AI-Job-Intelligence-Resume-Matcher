import streamlit as st

from src.resume_parser import extract_text_from_pdf
from src.matcher import calculate_match
from src.database import (
    initialize_database,
    save_analysis,
    get_analysis_history,
)


st.set_page_config(
    page_title="AI Job Intelligence",
    page_icon="🎯",
    layout="wide",
)

initialize_database()

st.title("🎯 AI Job Intelligence & Resume Matcher")
st.write(
    "Compare a resume with a job description, "
    "review skill gaps, and track previous analyses."
)

st.caption(
    "Scores are estimates based on text similarity and detected skills. "
    "They are not a hiring recommendation."
)

tab_analyze, tab_history = st.tabs(
    ["Resume Analyzer", "Analysis History"]
)

with tab_analyze:
    uploaded_file = st.file_uploader(
        "Upload a resume PDF",
        type=["pdf"],
    )

    job_title = st.text_input(
        "Job title",
        placeholder="Python Developer",
    )

    job_description = st.text_area(
        "Job description",
        height=220,
        placeholder=(
            "Paste the responsibilities, required skills, "
            "and qualifications from the job description..."
        ),
    )

    if st.button("Analyze Resume", type="primary"):
        if uploaded_file is None:
            st.error("Please upload a PDF resume.")

        elif not job_description.strip():
            st.error("Please enter a job description.")

        else:
            try:
                with st.spinner("Analyzing resume..."):
                    resume_text = extract_text_from_pdf(
                        uploaded_file
                    )

                    results = calculate_match(
                        resume_text,
                        job_description,
                    )

                st.subheader("Match Results")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Overall Match",
                    f'{results["match_score"]:.2f}%',
                )

                col2.metric(
                    "Text Similarity",
                    f'{results["text_similarity"]:.2f}%',
                )

                col3.metric(
                    "Skills Matched",
                    f'{len(results["matched_skills"])} / '
                    f'{len(results["job_skills"])}',
                )

                st.progress(
                    min(
                        1.0,
                        max(0.0, results["match_score"] / 100),
                    )
                )

                st.caption(
                    f'Matching method: {results["matching_method"]}'
                )

                left, right = st.columns(2)

                with left:
                    st.subheader("✅ Matching Skills")

                    if results["matched_skills"]:
                        for skill in results["matched_skills"]:
                            st.write(f"• {skill}")
                    else:
                        st.write("No matching skills detected.")

                with right:
                    st.subheader("📌 Skills to Develop")

                    if results["missing_skills"]:
                        for skill in results["missing_skills"]:
                            st.write(f"• {skill}")
                    else:
                        st.write(
                            "No missing skills detected from "
                            "the built-in skill list."
                        )

                with st.expander("Skills detected in resume"):
                    st.write(
                        results["resume_skills"]
                        or "No known skills detected."
                    )

                with st.expander("Skills detected in job description"):
                    st.write(
                        results["job_skills"]
                        or "No known skills detected."
                    )

                save_analysis(
                    resume_name=uploaded_file.name,
                    job_title=job_title.strip() or "Not specified",
                    results=results,
                )

                st.success("Analysis saved to local history.")

            except ValueError as error:
                st.error(str(error))

            except Exception as error:
                st.error(f"Analysis failed: {error}")


with tab_history:
    st.subheader("Recent Analyses")

    history = get_analysis_history()

    if not history:
        st.info("No analyses saved yet. Analyze a resume first.")
    else:
        for item in history:
            with st.expander(
                f'{item["job_title"]} — {item["match_score"]:.2f}%'
            ):
                st.write(f'Resume: {item["resume_name"]}')
                st.write(f'Date: {item["created_at"]}')
                st.write(f'Method: {item["matching_method"]}')
                st.write(
                    "Matching skills: "
                    + ", ".join(__import__("json").loads(
                        item["matched_skills"]
                    ))
                )
                st.write(
                    "Missing skills: "
                    + ", ".join(__import__("json").loads(
                        item["missing_skills"]
                    ))
                )
