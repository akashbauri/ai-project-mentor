from groq import Groq
import streamlit as st
import json

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


def clean_text(text):

    text = text.replace("\n", " ")

    if len(text) > 5000:
        text = text[:5000]

    return text


def generate_projects(text):

    text = clean_text(text)

    prompt = f"""
Analyze the learning material.

Return ONLY valid JSON in this format:

{{
 "skills": {{
   "Python": 80,
   "Pandas": 70
 }},
 "readiness_score": 75,
 "projects": [
   {{
     "name": "Example Project",
     "difficulty": "Intermediate",
     "tools": ["Python","Pandas"],
     "description": "Short description"
   }}
 ]
}}

Learning Material:
{text}
"""

    try:

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Return JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=800
        )

        output = completion.choices[0].message.content

        return json.loads(output)

    except Exception as e:

        return {
            "skills": {"Python":50},
            "readiness_score":50,
            "projects":[{"name":"AI Project","difficulty":"Medium","tools":["Python"],"description":"Example"}]
        }
