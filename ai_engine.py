from groq import Groq
import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


def split_text(text, chunk_size=2000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def summarize_chunk(chunk):

    prompt = f"""
Extract important technical skills from this learning material.

Return only skill names separated by commas.

Text:
{chunk}
"""

    try:

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You extract technical skills."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=200
        )

        return completion.choices[0].message.content

    except:

        return ""


def generate_projects(text):

    if not text or text.strip() == "":
        return "No readable learning material found."

    chunks = split_text(text)

    skill_summary = ""

    for chunk in chunks[:5]:

        skills = summarize_chunk(chunk)

        skill_summary += skills + "\n"


    final_prompt = f"""
A learner studied the following topics:

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
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You help learners build coding projects."},
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.2,
            max_tokens=900
        )

        return completion.choices[0].message.content

    except Exception as e:

        return f"AI generation failed: {str(e)}"
