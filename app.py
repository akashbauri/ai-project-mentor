import streamlit as st
import pandas as pd
import plotly.express as px

from file_parser import extract_text, extract_from_url
from ai_engine import generate_projects
from pdf_generator import create_pdf
from repo_generator import create_repo_zip


# Page config
st.set_page_config(
    page_title="AI Project Mentor",
    page_icon="🤖",
    layout="wide"
)


# Title
st.title("AI Project Mentor")


# Description
st.markdown("""
### Created by **Akash Bauri**

AI Project Mentor converts learning material into **real-world software projects**.

Upload learning material or paste a tutorial link and the system will:

- Detect technical skills
- Generate project ideas
- Show AI-powered skill dashboard
- Calculate **Project Readiness Score**
- Provide starter code
- Generate GitHub repository
- Export project documentation
""")


# File uploader
uploaded_files = st.file_uploader(
    "Upload learning material (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)


# URL input
url_input = st.text_input(
    "Or paste a website / YouTube tutorial link"
)


all_text = ""


# Extract text from uploaded files
if uploaded_files:

    for file in uploaded_files:

        file_text = extract_text(file)

        all_text += file_text + " "


# Extract text from URL
if url_input:

    url_text = extract_from_url(url_input)

    all_text += url_text + " "


# Analyze button
if st.button("Analyze Learning Material"):

    if all_text.strip() == "":

        st.warning("Please upload a document or paste a tutorial link.")

    else:

        with st.spinner("Analyzing learning material using AI..."):

            result = generate_projects(all_text)


        # -----------------------------
        # Skill Dashboard
        # -----------------------------

        skills = result.get("skills", {})

        if skills:

            df = pd.DataFrame(
                list(skills.items()),
                columns=["Skill", "Percentage"]
            )

            fig = px.bar(
                df,
                x="Skill",
                y="Percentage",
                title="Skill Distribution",
                color="Skill"
            )

            st.subheader("Skill Dashboard")

            st.plotly_chart(fig, use_container_width=True)


        # -----------------------------
        # Readiness Score
        # -----------------------------

        readiness = result.get("readiness_score", 50)

        st.subheader("Project Readiness Score")

        st.progress(readiness / 100)

        st.write(f"Readiness Score: **{readiness}%**")


        # -----------------------------
        # Projects
        # -----------------------------

        st.subheader("Recommended Projects")

        projects = result.get("projects", [])

        for p in projects:

            st.markdown(f"### {p.get('name','Project')}")

            st.write("**Difficulty:**", p.get("difficulty","Unknown"))

            tools = p.get("tools", [])

            if tools:
                st.write("**Tools:**", ", ".join(tools))

            st.write("**Description:**", p.get("description",""))

            st.write("**Architecture:**")
            st.code(p.get("architecture",""))

            st.write("**Folder Structure:**")
            st.code(p.get("folder_structure",""))

            st.write("**Starter Code:**")
            st.code(p.get("starter_code",""), language="python")

            st.divider()


        # -----------------------------
        # PDF Generation
        # -----------------------------

        pdf_file = create_pdf(str(result), "project_documentation.pdf")

        with open(pdf_file, "rb") as file:

            st.download_button(
                "Download Project Documentation (PDF)",
                data=file,
                file_name="project_documentation.pdf",
                mime="application/pdf"
            )


        # -----------------------------
        # GitHub Repo Generator
        # -----------------------------

        repo_zip = create_repo_zip("ai_generated_project")

        with open(repo_zip, "rb") as file:

            st.download_button(
                "Download GitHub Project Repository",
                data=file,
                file_name="ai_project_repo.zip",
                mime="application/zip"
            )
