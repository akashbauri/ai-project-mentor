from groq import Groq
import streamlit as st

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])


def clean_text(text):
    """
    Clean extracted text and limit size to avoid token overflow.
    """
    text = text.replace("\n", " ")

    if len(text) > 5000:
        text = text[:5000]

    return text


def generate_projects(text):
    """
    Send learning material to Groq and generate projects.
    """

    text = clean_text(text)

    prompt = f"""
You are a senior software engineer and mentor.

A learner uploaded learning material from tutorials, PDFs, websites, or videos.

Your tasks:

1. Identify all technical skills mentioned.
2. Estimate skill proficiency percentages.
3. Calculate a learner readiness score.
4. Generate three practical software projects the learner can build.
5. Provide documentation and working starter code.

Respond using THIS STRUCTURE EXACTLY.

--------------------------------------------------

SKILLS

Python - 80
Pandas - 70
Machine Learning - 60
Data Visualization - 65

--------------------------------------------------

READINESS_SCORE

75

--------------------------------------------------

PROJECT 1

NAME
Project Name

DIFFICULTY
Beginner / Intermediate / Advanced

TOOLS
Python, Pandas, Scikit-learn

DESCRIPTION
Short explanation of the project.

DOCUMENTATION
Step by step explanation of how to build the project.

ARCHITECTURE
Explain the system architecture.

FOLDER_STRUCTURE
project/
  data/
  src/
  models/

STARTER_CODE

import pandas as pd
print("project starter")

--------------------------------------------------

Repeat the same structure for PROJECT 2 and PROJECT 3.

--------------------------------------------------

Learning material:
{text}
"""

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are an expert programming mentor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1800
    )

    return completion.choices[0].message.content
