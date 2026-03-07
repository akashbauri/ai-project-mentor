from groq import Groq
import streamlit as st
import json
import re

# Initialize Groq client using Streamlit secret
client = Groq(api_key=st.secrets["GROQ_API_KEY"])


def clean_text(text):
    """
    Clean and limit text to avoid token overflow.
    """
    text = text.replace("\n", " ")

    if len(text) > 5000:
        text = text[:5000]

    return text


def extract_json(text):
    """
    Extract JSON object from model response safely.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group(0)

    return None


def generate_projects(text):
    """
    Send learning material to Groq Llama3-70B and
    return structured project ideas.
    """

    text = clean_text(text)

    prompt = f"""
You are a senior AI software architect.

Analyze the learning material and generate 3 real software projects.

Return ONLY valid JSON.

JSON format:

{{
 "skills": {{
   "Python": 80,
   "Pandas": 70
 }},
 "readiness_score": 75,
 "projects": [
   {{
     "name": "Stock Price Prediction System",
     "difficulty": "Intermediate",
     "tools": ["Python", "Pandas", "Scikit-learn"],
     "description": "Predict stock prices using machine learning.",
     "architecture": "Data → Model → Prediction → Visualization",
     "folder_structure": "project/ data/ src/ models/ notebook.ipynb",
     "starter_code": "import pandas as pd"
   }}
 ]
}}

Learning material:
{text}
"""

    try:

        completion = client.chat.completions.create(
            model="llama3-70b-8192",  # Updated model
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=1500
        )

        output = completion.choices[0].message.content

        json_text = extract_json(output)

        return json.loads(json_text)

    except Exception as e:

        # fallback result if parsing fails
        return {
            "skills": {"Python": 50},
            "readiness_score": 50,
            "projects": [
                {
                    "name": "Example Project",
                    "difficulty": "Medium",
                    "tools": ["Python"],
                    "description": "Fallback example",
                    "architecture": "Example architecture",
                    "folder_structure": "src/",
                    "starter_code": "print('example')"
                }
            ]
        }
