import streamlit as st
import pandas as pd
import plotly.express as px

from file_parser import extract_text, extract_from_url
from ai_engine import generate_projects
from pdf_generator import create_pdf
from repo_generator import create_repo_zip


st.title("AI Project Mentor")

st.markdown("### Created by Akash Bauri")

st.write(
"""
Upload learning materials or tutorial links.

The system will:

• detect technical skills  
• calculate readiness score  
• generate 3 projects  
• provide documentation and starter code
"""
)


# ----------------------------------
# FILE INPUT SECTION
# ----------------------------------

st.subheader("Upload Learning Files")

uploaded_files = st.file_uploader(
    "Upload PPT, PDF, or Word files",
    type=["pdf","docx","pptx"],
    accept_multiple_files=True
)


# ----------------------------------
# WEBSITE INPUT
# ----------------------------------

st.subheader("Website Link")

website_link = st.text_input(
    "Paste website tutorial link"
)


# ----------------------------------
# YOUTUBE INPUT
# ----------------------------------

st.subheader("YouTube Link")

youtube_link = st.text_input(
    "Paste YouTube tutorial link"
)


all_text = ""


# Extract from uploaded files
if uploaded_files:

    for file in uploaded_files:

        text = extract_text(file)

        all_text += text + " "


# Extract website text
if website_link:

    website_text = extract_from_url(website_link)

    all_text += website_text + " "


# Extract youtube transcript
if youtube_link:

    youtube_text = extract_from_url(youtube_link)

    all_text += youtube_text + " "


# ----------------------------------
# ANALYZE BUTTON
# ----------------------------------

if st.button("Analyze Learning Material"):

    if all_text.strip() == "":

        st.warning("Please upload files or paste links.")

    else:

        with st.spinner("Analyzing with AI..."):

            result = generate_projects(all_text)


        # ----------------------------------
        # SKILL DASHBOARD
        # ----------------------------------

        skills = result.get("skills",{})

        df = pd.DataFrame(
            list(skills.items()),
            columns=["Skill","Percentage"]
        )

        fig = px.bar(
            df,
            x="Skill",
            y="Percentage",
            title="Detected Skills"
        )

        st.subheader("Skill Dashboard")

        st.plotly_chart(fig)


        # ----------------------------------
        # READINESS SCORE
        # ----------------------------------

        readiness = result.get("readiness_score",50)

        st.subheader("Project Readiness Score")

        st.progress(readiness/100)

        st.write(f"Score: {readiness}%")


        # ----------------------------------
        # PROJECT OUTPUT
        # ----------------------------------

        st.subheader("Generated Projects")

        for p in result["projects"]:

            st.markdown(f"### {p['name']}")

            st.write("Difficulty:",p["difficulty"])

            st.write("Tools:",", ".join(p["tools"]))

            st.write("Description:",p["description"])

            st.write("Documentation")

            st.write(p["documentation"])

            st.write("Architecture")

            st.code(p["architecture"])

            st.write("Folder Structure")

            st.code(p["folder_structure"])

            st.write("Starter Code")

            st.code(p["starter_code"],language="python")

            st.divider()


        # ----------------------------------
        # DOWNLOADS
        # ----------------------------------

        pdf_file = create_pdf(str(result),"project_documentation.pdf")

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
