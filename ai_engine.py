from groq import Groq
import streamlit as st


client = Groq(api_key=st.secrets["GROQ_API_KEY"])


def clean_text(text):

    text = text.replace("\n", " ")

    if len(text) > 5000:
        text = text[:5000]

    return text


def generate_projects(text):

    text = clean_text(text)

    prompt = f"""
You are an AI software mentor.

Analyze the learning material.

1. Detect the main programming language.
2. Extract technical skills.
3. Estimate skill percentages.
4. Calculate a Project Readiness Score (0-100).
5. Suggest 3 practical projects.

For each project include:
- project name
- difficulty
- tools
- GitHub-ready folder structure
- step-by-step build plan
- starter code

Learning Material:
{text}
"""

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an expert AI engineering mentor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=2000
    )

    return completion.choices[0].message.content
