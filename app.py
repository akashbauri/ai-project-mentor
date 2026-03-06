import streamlit as st
import pandas as pd
import plotly.express as px

from file_parser import extract_text
from ai_engine import generate_projects
from pdf_generator import create_pdf

st.title("AI Project Mentor")

st.write("Upload learning material and generate real projects.")

uploaded_file = st.file_uploader(
    "Upload PDF or DOCX",
    type=["pdf","docx"]
)

if uploaded_file:

    text = extract_text(uploaded_file)

    st.success("Material uploaded successfully")

    if st.button("Analyze and Generate Projects"):

        result = generate_projects(text)

        st.subheader("AI Generated Output")

        st.write(result)

        # Example skill dashboard
        skills = {
            "Python":80,
            "Pandas":70,
            "Machine Learning":50,
            "Visualization":60
        }

        df = pd.DataFrame(
            list(skills.items()),
            columns=["Skill","Percentage"]
        )

        fig = px.bar(df,x="Skill",y="Percentage")

        st.subheader("Skill Dashboard")

        st.plotly_chart(fig)

        pdf_file = create_pdf(result,"project_plan.pdf")

        with open(pdf_file,"rb") as file:

            st.download_button(
                "Download Project Documentation",
                data=file,
                file_name="project_plan.pdf",
                mime="application/pdf"
            )
