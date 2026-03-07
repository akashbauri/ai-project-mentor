import streamlit as st
import pandas as pd
import plotly.express as px

from file_parser import extract_text, extract_from_url
from ai_engine import generate_projects
from pdf_generator import create_pdf
from repo_generator import create_repo_zip


st.set_page_config(page_title="AI Project Mentor", layout="wide")

st.title("AI Project Mentor")

st.markdown("""
### Created by **Akash Bauri**

Upload learning material (PDF, DOCX, YouTube, Website).

The AI will:

• detect skills  
• calculate readiness score  
• generate **3 software projects**  
• provide **documentation + starter code**  
""")


uploaded_files = st.file_uploader(
    "Upload learning material (PDF or DOCX)",
    type=["pdf","docx"],
    accept_multiple_files=True
)

url_input = st.text_input(
    "Or paste a website / YouTube tutorial link"
)


all_text = ""


if uploaded_files:

    for file in uploaded_files:

        text = extract_text(file)

        all_text += text + " "


if url_input:

    url_text = extract_from_url(url_input)

    all_text += url_text + " "


if st.button("Analyze Learning Material"):

    if all_text.strip() == "":

        st.warning("Please upload a file or paste a link.")

    else:

        with st.spinner("AI analyzing material..."):

            result = generate_projects(all_text)


        # ---------------------
        # Skill Dashboard
        # ---------------------

        skills = result.get("skills", {})

        if skills:

            df = pd.DataFrame(
                list(skills.items()),
                columns=["Skill","Percentage"]
            )

            fig = px.bar(
                df,
                x="Skill",
                y="Percentage",
                title="Skill Distribution"
            )

            st.subheader("Skill Dashboard")

            st.plotly_chart(fig, use_container_width=True)


        # ---------------------
        # Readiness Score
        # ---------------------

        readiness = result.get("readiness_score", 50)

        st.subheader("Project Readiness Score")

        st.progress(readiness/100)

        st.write(f"Readiness Score: **{readiness}%**")


        # ---------------------
        # Projects
        # ---------------------

        st.subheader("Generated Projects")

        for p in result["projects"]:

            st.markdown(f"### {p['name']}")

            st.write("Difficulty:", p["difficulty"])

            st.write("Tools:", ", ".join(p["tools"]))

            st.write("Description:", p["description"])

            st.write("Documentation:")
            st.write(p["documentation"])

            st.write("Architecture:")
            st.code(p["architecture"])

            st.write("Folder Structure:")
            st.code(p["folder_structure"])

            st.write("Starter Code:")
            st.code(p["starter_code"], language="python")

            st.divider()


        # ---------------------
        # Download PDF
        # ---------------------

        pdf_file = create_pdf(str(result),"project_documentation.pdf")

        with open(pdf_file,"rb") as file:

            st.download_button(
                "Download Project Documentation (PDF)",
                data=file,
                file_name="project_documentation.pdf",
                mime="application/pdf"
            )


        # ---------------------
        # Download GitHub Repo
        # ---------------------

        repo_zip = create_repo_zip("ai_generated_project")

        with open(repo_zip,"rb") as file:

            st.download_button(
                "Download GitHub Repository",
                data=file,
                file_name="ai_project_repo.zip",
                mime="application/zip"
            )
