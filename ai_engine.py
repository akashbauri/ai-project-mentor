from groq import Groq
import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


def extract_skills_locally(text):

    skill_keywords = {
        "Python": ["python"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        "Machine Learning": ["machine learning","scikit","sklearn"],
        "Data Visualization": ["matplotlib","seaborn"],
        "SQL": ["sql"],
        "Deep Learning": ["deep learning","tensorflow","pytorch"],
        "Statistics": ["statistics","probability"]
    }

    text = text.lower()

    detected = []

    for skill, keywords in skill_keywords.items():

        for k in keywords:

            if k in text:

                detected.append(skill)

                break

    return detected


def generate_projects(text):

    if not text or text.strip() == "":
        return "No readable learning material found."

    skills = extract_skills_locally(text)

    skill_summary = ", ".join(skills)

    prompt = f"""
A learner studied these topics:

{skill_summary}

Generate 3 practical software projects they can build.

For each project include:

PROJECT NAME
TOOLS
DESCRIPTION
DOCUMENTATION
STARTER_CODE

Keep explanations concise.
"""

    try:

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You help learners build coding projects."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=900
        )

        return completion.choices[0].message.content

    except Exception as e:

        return f"AI generation failed: {str(e)}"
