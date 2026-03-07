import streamlit as st
import pandas as pd
import plotly.express as px

from file_parser import extract_text, extract_from_url
from ai_engine import generate_projects
from pdf_generator import create_pdf
from repo_generator import create_repo_zip


st.set_page_config(layout="wide")

st.title("AI Project Mentor")

st.markdown("### Created by Akash Bauri")


# FILE UPLOAD
st.subheader("Upload Learning Files")

uploaded_files = st.file_uploader(
    "Upload PPT / PDF / Word",
    type=["pdf","docx","pptx"],
    accept_multiple_files=True
)


# WEBSITE
st.subheader("Website Link")

website_link = st.text_input(
    "Paste website tutorial link"
)


# YOUTUBE
st.subheader("YouTube Link")

youtube_link = st.text_input(
    "Paste YouTube tutorial link"
)


all_text = ""


if uploaded_files:

    for file in uploaded_files:

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

        st.warning("Please upload files or paste links.")

    else:

        with st.spinner("Analyzing with AI..."):

            result = generate_projects(all_text)

        st.markdown(result)


        # Skill Dashboard
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
                columns=["Skill","Score"]
            )

            fig = px.bar(
                df,
                x="Skill",
                y="Score",
                title="Detected Skills"
            )

            st.subheader("Skill Dashboard")

            st.plotly_chart(fig)


        # PDF DOWNLOAD
        pdf_file = create_pdf(result,"project_documentation.pdf")

        with open(pdf_file,"rb") as file:

            st.download_button(
                "Download Project Documentation",
                data=file,
                file_name="project_documentation.pdf",
                mime="application/pdf"
            )


        # REPO DOWNLOAD
        repo_zip = create_repo_zip("ai_generated_project")

        with open(repo_zip,"rb") as file:

            st.download_button(
                "Download GitHub Repository",
                data=file,
                file_name="ai_project_repo.zip",
                mime="application/zip"
            )
