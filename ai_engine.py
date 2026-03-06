from groq import Groq
import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def generate_projects(text):

    prompt = f"""
You are an AI project mentor.

Analyze the following learning material.

1. Extract skills.
2. Estimate skill percentages.
3. Suggest 3 projects.
4. For each project include:
- name
- difficulty
- tools
- step-by-step build plan
- starter code

Learning Material:
{text}
"""

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content
