from groq import Groq
import streamlit as st

# Initialize Groq client using Streamlit secret
client = Groq(api_key=st.secrets["GROQ_API_KEY"])


def clean_text(text):
    """
    Clean extracted text and limit length to prevent token overflow.
    """
    text = text.replace("\n", " ")

    # Limit input size for stability
    if len(text) > 5000:
        text = text[:5000]

    return text


def generate_projects(text):
    """
    Send learning material to Groq Llama3-70B
    and return structured Markdown output.
    """

    text = clean_text(text)

    prompt = f"""
You are a senior software engineer and technical mentor.

A learner uploaded learning material (PDF, PPT, Word, website, or YouTube transcript).

Your tasks:

1. Identify ALL technical skills mentioned
2. Estimate skill proficiency percentages
3. Calculate a learner readiness score
4. Generate 3 real software projects the learner can build
5. Provide documentation and working starter code

IMPORTANT RULES:
- Respond ONLY using Markdown
- Follow the structure EXACTLY
- Provide REALISTIC project ideas
- Starter code must be valid Python

Use this format:

---

## SKILLS

Python - 80  
Pandas - 70  
Machine Learning - 60  
Data Visualization - 65  

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
Step-by-step explanation of how to build the project.

### ARCHITECTURE
Explain the system architecture.

### FOLDER_STRUCTURE
project/
  data/
  src/
  models/

### STARTER_CODE

```python
# example starter code
import pandas as pd
print("project starter")

PROJECT 2

(Use the same structure)

PROJECT 3

(Use the same structure)

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
