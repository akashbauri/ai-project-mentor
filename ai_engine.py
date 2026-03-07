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
You are a senior software engineer mentor.

A learner uploaded learning material.

Your task:

1. Identify ALL technical skills mentioned
2. Estimate skill percentages
3. Generate 3 buildable software projects
4. Provide documentation and working starter code

Respond using THIS STRUCTURE EXACTLY.

---

## SKILLS

Python - 80  
Pandas - 70  
Machine Learning - 60  

---

## READINESS_SCORE

75

---

## PROJECT 1

### NAME
Project Name

### DIFFICULTY
Beginner / Intermediate / Advanced

### TOOLS
Python, Pandas, Scikit-learn

### DESCRIPTION
Short explanation of the project.

### DOCUMENTATION
Step by step explanation of how to build it.

### ARCHITECTURE
Explain system architecture.

### FOLDER_STRUCTURE
project/
  data/
  src/
  models/

### STARTER_CODE

```python
your working python code here


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

    
