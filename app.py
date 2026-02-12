import streamlit as st
from pathlib import Path
import tempfile

from parsers.resume_parser import ResumeParser
from extractors.keyword_extractor import KeywordExtractor
from matcher.scoring_engine import ScoringEngine


st.title("AI Resume Screening System")

jd_text = st.text_area(
    "Paste the job description here:",
    height=300
)

uploaded_files = st.file_uploader(
    "Upload resume files:",
    type=["pdf", "docx"],
    accept_multiple_files=True
)


if st.button("Screen Resumes", type="primary"):

    if not jd_text:
        st.warning("Please enter a job description.")
        st.stop()

    if not uploaded_files:
        st.warning("Please upload at least one resume.")
        st.stop()

    st.success("Processing resumes...")

    parser = ResumeParser()
    extractor = KeywordExtractor()

    # Example job requirements (static for now)
    required_skills = {"Python", "Machine Learning"}
    preferred_skills = {"Django", "TensorFlow"}
    experience_keywords = ["years", "experience", "worked"]
    domain_keywords = ["AI", "data", "model"]

    scoring_engine = ScoringEngine(
        required_skills,
        preferred_skills,
        experience_keywords,
        domain_keywords
    )

    results = []

    for uploaded_file in uploaded_files:

        # Preserve original file extension
        file_suffix = Path(uploaded_file.name).suffix

        # Save temporarily with correct extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = Path(tmp_file.name)

        # Now process resume
        resume_text = parser.extract_text(tmp_path)
        resume_skills = extractor.extract_skills(resume_text)

        score = scoring_engine.calculate_score(
            resume_skills,
            resume_text
        )

        results.append((uploaded_file.name, score, resume_skills))

    # Sort by score descending
    results.sort(key=lambda x: x[1], reverse=True)

    st.subheader("Ranking Results")

    for rank, (name, score, skills) in enumerate(results, start=1):
        st.write(f"### Rank #{rank}")
        st.write(f"**File:** {name}")
        st.write(f"**Score:** {score}/100")
        st.write(f"**Matched Skills:** {', '.join(skills) if skills else 'None'}")
        st.markdown("---")
