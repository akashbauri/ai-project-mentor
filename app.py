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

st.write(
"""
Upload learning materials and the AI will generate projects.

Supported inputs:
- PDF
- Word (DOCX)
- PowerPoint (PPTX)
- Website links
- YouTube tutorials
"""
)

st.info("Maximum file size allowed: **5 MB per file**")


# ----------------------------
# FILE UPLOAD SECTION
# ----------------------------

st.subheader("Upload Learning Files")

uploaded_files = st.file_uploader(
    "Upload PDF / Word / PPT files",
    type=["pdf", "docx", "pptx"],
    accept_multiple_files=True
)


# ----------------------------
# WEBSITE LINK
# ----------------------------

st.subheader("Website Link")

website_link = st.text_input(
    "Paste a tutorial website link"
)


# ----------------------------
# YOUTUBE LINK
# ----------------------------

st.subheader("YouTube Link")

youtube_link = st.text_input(
    "Paste a YouTube tutorial link"
)


all_text = ""

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


# ----------------------------
# PROCESS FILES
# ----------------------------

if uploaded_files:

    for file in uploaded_files:

        if file.size > MAX_FILE_SIZE:

            st.error(f"{file.name} exceeds the 5 MB limit.")
            st.stop()

        text = extract_text(file)

        all_text += text + " "


# ----------------------------
# PROCESS WEBSITE
# ----------------------------

if website_link:

    website_text = extract_from_url(website_link)

    all_text += website_text + " "


# ----------------------------
# PROCESS YOUTUBE
# ----------------------------

if youtube_link:

    youtube_text = extract_from_url(youtube_link)

    all_text += youtube_text + " "


# ----------------------------
# ANALYZE BUTTON
# ----------------------------

if st.button("Analyze Learning Material"):

    if all_text.strip() == "":

        st.warning("Please upload files or paste links.")

    else:

        with st.spinner("Analyzing learning material with AI..."):

            result = generate_projects(all_text)

        st.subheader("AI Generated Projects")

        st.markdown(result)


        # ----------------------------
        # SKILL DASHBOARD
        # ----------------------------

        skills = {}

        lines = result.split("\n")

        for line in lines:

            if "-" in line:

                parts = line.split("-")

                if len(parts) == 2:

                    skill = parts[0].strip()

                    try:
                        score = int(parts[1].strip())
                        skills[skill] = score
                    except:
                        pass


        if skills:

            df = pd.DataFrame(
                list(skills.items()),
                columns=["Skill", "Score"]
            )

            fig = px.bar(
                df,
                x="Skill",
                y="Score",
                title="Detected Technical Skills"
            )

            st.subheader("Skill Dashboard")

            st.plotly_chart(fig, use_container_width=True)


        # ----------------------------
        # DOWNLOAD PDF
        # ----------------------------

        pdf_file = create_pdf(result, "project_documentation.pdf")

        with open(pdf_file, "rb") as file:

            st.download_button(
                "Download Project Documentation (PDF)",
                data=file,
                file_name="project_documentation.pdf",
                mime="application/pdf"
            )


        # ----------------------------
        # DOWNLOAD REPO
        # ----------------------------

        repo_zip = create_repo_zip("ai_generated_project")

        with open(repo_zip, "rb") as file:

            st.download_button(
                "Download GitHub Repository",
                data=file,
                file_name="ai_project_repo.zip",
                mime="application/zip"
            )
