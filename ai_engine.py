from groq import Groq
import streamlit as st
import json
import re

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


def clean_text(text):
    text = text.replace("\n", " ")
    if len(text) > 5000:
        text = text[:5000]
    return text


def extract_json(text):
    """
    Safely extract JSON from model output.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return None


def generate_projects(text):

    text = clean_text(text)

    prompt = f"""
You are an expert software architect.

From the learning material identify ALL programming and technical skills.

Then generate 3 real projects.

Return ONLY JSON.

JSON format:

{{
 "skills": {{
   "Python":80,
   "Pandas":70,
   "Machine Learning":65,
   "Data Visualization":60
 }},
 "readiness_score":75,
 "projects":[
   {{
    "name":"Project Name",
    "difficulty":"Beginner/Intermediate/Advanced",
    "tools":["Python","Library"],
    "description":"Project explanation",
    "documentation":"Step-by-step implementation guide",
    "architecture":"System architecture",
    "folder_structure":"project/data project/src",
    "starter_code":"Python code"
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
                {"role": "system", "content": "Return JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1200
        )

        output = completion.choices[0].message.content

        json_text = extract_json(output)

        return json.loads(json_text)

    except Exception as e:

        return {
            "skills":{"Python":50},
            "readiness_score":50,
            "projects":[
                {
                    "name":"Example Project",
                    "difficulty":"Medium",
                    "tools":["Python"],
                    "description":"Fallback example",
                    "documentation":"Example documentation",
                    "architecture":"Example architecture",
                    "folder_structure":"src/",
                    "starter_code":"print('example project')"
                }
            ]
        }
