import streamlit as st
import pandas as pd
import plotly.express as px

from file_parser import extract_text, extract_from_url
from ai_engine import generate_projects
from pdf_generator import create_pdf
from repo_generator import create_repo_zip


st.title("AI Project Mentor")

st.markdown("""
### Created by **Akash Bauri**

AI Project Mentor converts learning material into **real-world projects**.

Upload study material or paste a tutorial link and the system will:

• Detect skills  
• Generate project ideas  
• Show AI-powered skill dashboard  
• Calculate Project Readiness Score  
• Provide starter code  
• Generate GitHub repository  
• Export project documentation
""")


uploaded_files = st.file_uploader(
    "Upload learning material (PDF or DOCX)",
    type=["pdf","docx"],
    accept_multiple_files=True
)

url_input = st.text_input("Paste a website or YouTube link")

all_text = ""


# Extract text from files
if uploaded_files:

    for file in uploaded_files:

        file_text = extract_text(file)

        all_text += file_text


# Extract text from link
if url_input:

    url_text = extract_from_url(url_input)

    all_text += url_text


if st.button("Analyze Material"):

    if all_text.strip() == "":

        st.warning("Could not extract text from the file or link.")

    else:

        with st.spinner("Analyzing learning material..."):

            result = generate_projects(all_text)


        # Skill dashboard
        skills = result["skills"]

        df = pd.DataFrame(list(skills.items()), columns=["Skill","Percentage"])

        fig = px.bar(df,x="Skill",y="Percentage",title="Skill Distribution")

        st.subheader("Skill Dashboard")

        st.plotly_chart(fig)


        # Readiness score
        readiness = result["readiness_score"]

        st.subheader("Project Readiness Score")

        st.progress(readiness/100)

        st.write(f"Readiness Score: {readiness}%")


        # Projects
        st.subheader("Recommended Projects")

        for p in result["projects"]:

            st.markdown(f"### {p['name']}")

            st.write("Difficulty:",p["difficulty"])

            st.write("Tools:",", ".join(p["tools"]))

            st.write(p["description"])


        # Generate PDF
        pdf_file = create_pdf(str(result),"project_documentation.pdf")

        with open(pdf_file,"rb") as file:

            st.download_button(
                "Download Project Documentation",
                data=file,
                file_name="project_documentation.pdf",
                mime="application/pdf"
            )


        # Generate GitHub repo
        repo_zip = create_repo_zip("ai_generated_project")

        with open(repo_zip,"rb") as file:

            st.download_button(
                "Download GitHub Repository",
                data=file,
                file_name="ai_project_repo.zip",
                mime="application/zip"
            )
