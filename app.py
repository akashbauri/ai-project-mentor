import streamlit as st
import pandas as pd
import plotly.express as px

from file_parser import extract_text, extract_from_url
from ai_engine import generate_projects
from pdf_generator import create_pdf
from repo_generator import create_repo_zip


st.set_page_config(page_title="AI Project Mentor", layout="wide")

st.title("AI Project Mentor")

st.markdown("### Created by Akash Bauri")

st.info("Maximum file size: 5 MB per file")


def detect_skills(text):

    skill_keywords = {
        "Python": ["python"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        "Machine Learning": ["machine learning","scikit","sklearn"],
        "Data Visualization": ["matplotlib","seaborn"],
        "SQL": ["sql"],
        "Deep Learning": ["deep learning","tensorflow","pytorch"]
    }

    text = text.lower()

    scores = {}

    for skill, keywords in skill_keywords.items():

        count = 0

        for k in keywords:

            count += text.count(k)

        if count > 0:

            scores[skill] = count

    if scores:

        max_score = max(scores.values())

        for skill in scores:

            scores[skill] = int((scores[skill] / max_score) * 100)

    return scores


uploaded_files = st.file_uploader(
    "Upload PDF / Word / PPT",
    type=["pdf","docx","pptx"],
    accept_multiple_files=True
)

website_link = st.text_input("Website Link")

youtube_link = st.text_input("YouTube Link")


all_text = ""

MAX_FILE_SIZE = 5 * 1024 * 1024


if uploaded_files:

    for file in uploaded_files:

        if file.size > MAX_FILE_SIZE:

            st.error(f"{file.name} exceeds 5 MB")

            st.stop()

        text = extract_text(file)

        all_text += text + " "


if website_link:

    website_text = extract_from_url(website_link)

    all_text += website_text + " "


if youtube_link:

    youtube_text = extract_from_url(youtube_link)

    all_text += youtube_text + " "


if st.button("Analyze Learning Material"):

    if all_text.strip() == "":

        st.warning("Upload files or paste links.")

    else:

        with st.spinner("Analyzing learning material..."):

            result = generate_projects(all_text)

        st.subheader("AI Generated Projects")

        st.markdown(result)


        skills = detect_skills(all_text)

        if skills:

            df = pd.DataFrame(
                list(skills.items()),
                columns=["Skill","Score"]
            )

            fig = px.bar(
                df,
                x="Skill",
                y="Score",
                title="Detected Skills"
            )

            st.subheader("Skill Dashboard")

            st.plotly_chart(fig, use_container_width=True)


        pdf_file = create_pdf(result,"project_documentation.pdf")

        with open(pdf_file,"rb") as file:

            st.download_button(
                "Download Project Documentation",
                data=file,
                file_name="project_documentation.pdf",
                mime="application/pdf"
            )


        repo_zip = create_repo_zip("ai_generated_project")

        with open(repo_zip,"rb") as file:

            st.download_button(
                "Download GitHub Repository",
                data=file,
                file_name="ai_project_repo.zip",
                mime="application/zip"
            )
