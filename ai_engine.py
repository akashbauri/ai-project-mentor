from groq import Groq
import streamlit as st
import json
import re

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


def clean_text(text):

    text = text.replace("\n", " ")

    # limit text to avoid token overflow
    if len(text) > 5000:
        text = text[:5000]

    return text


def extract_json(text):

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group(0)

    return None


def generate_projects(text):

    text = clean_text(text)

    prompt = f"""
You are a senior AI software engineer.

Analyze the learning material and generate 3 real software projects.

Return ONLY JSON.

Each project must include:

- name
- difficulty
- tools
- description
- documentation (step by step guide)
- architecture
- folder_structure
- starter_code (real working Python code)

JSON format:

{{
 "skills": {{"Python":80,"Pandas":70}},
 "readiness_score":75,
 "projects":[
   {{
     "name":"Stock Price Prediction System",
     "difficulty":"Intermediate",
     "tools":["Python","Pandas","Scikit-learn"],
     "description":"Predict stock prices using machine learning.",
     "documentation":"Step 1 load data, Step 2 train model...",
     "architecture":"Data → Model → Prediction → Visualization",
     "folder_structure":"project/data project/src project/models",
     "starter_code":"import pandas as pd"
   }}
 ]
}}

Learning material:
{text}
"""

    try:

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1500
        )

        output = completion.choices[0].message.content

        json_text = extract_json(output)

        return json.loads(json_text)

    except Exception:

        return {
            "skills": {"Python": 50},
            "readiness_score": 50,
            "projects": [
                {
                    "name": "Example Project",
                    "difficulty": "Medium",
                    "tools": ["Python"],
                    "description": "Fallback example",
                    "documentation": "Example documentation",
                    "architecture": "Example architecture",
                    "folder_structure": "src/",
                    "starter_code": "print('example project')"
                }
            ]
        }
