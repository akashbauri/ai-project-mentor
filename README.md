# 🚀 AI Project Mentor

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Groq](https://img.shields.io/badge/LLM-Groq-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**AI Project Mentor** is an AI-powered tool that helps learners convert their learning materials into **real, buildable projects**.

Many learners complete courses, read documentation, or watch tutorials but still struggle to start building something on their own. AI Project Mentor bridges that gap by transforming learning content into **structured projects with step-by-step implementation guidance**.

---

# 📌 Problem

Many learners experience what can be called the **Silent Learning Gap**.

Even after finishing courses, learners often feel stuck because they do not know:

* what project they should build
* how to start building
* which tools to use
* how to structure a project

As a result, knowledge stays theoretical and never becomes practical experience.

---

# 💡 Solution

AI Project Mentor analyzes learning materials and converts them into **actionable projects**.

Users upload learning resources such as:

* PDF course notes
* Word documents
* tutorials or study material

The AI system extracts the key skills from the material and generates **practical projects that the learner can build immediately**.

---

# ✨ Features

✔ Upload learning materials (PDF / DOCX)
✔ AI-powered skill extraction
✔ Skill distribution dashboard
✔ AI-generated project ideas
✔ Step-by-step project build plan
✔ Starter code generation
✔ Downloadable project documentation (PDF)

---

# ⚙️ Example Workflow

### Step 1 — Upload Learning Material

Upload a document containing course notes or tutorials.

```
Python Data Science Notes.pdf
```

---

### Step 2 — Skill Detection

The AI analyzes the document and detects key skills such as:

* Python
* Pandas
* Data Visualization
* Machine Learning

---

### Step 3 — Skill Dashboard

The application visualizes the detected skills.

Example:

| Skill            | Usage |
| ---------------- | ----- |
| Python           | 80%   |
| Pandas           | 70%   |
| Visualization    | 60%   |
| Machine Learning | 40%   |

---

### Step 4 — AI Generated Projects

Example project:

**Stock Price Prediction System**

Difficulty: Intermediate

Tools Required:

* Python
* Pandas
* Scikit-learn
* Matplotlib
* Jupyter Notebook

---

### Step 5 — Step-by-Step Build Guide

Each project includes a clear execution plan.

Example:

1. Download historical stock dataset
2. Load data using Pandas
3. Clean and preprocess the data
4. Train a Linear Regression model
5. Visualize predictions using Matplotlib
6. Evaluate model performance

---

### Step 6 — Starter Code

```python
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

data = pd.read_csv("stock_data.csv")

X = data[['Open','High','Low']]
y = data['Close']

model = LinearRegression()
model.fit(X,y)

predictions = model.predict(X)

plt.plot(y,label="Actual")
plt.plot(predictions,label="Predicted")
plt.legend()
plt.show()
```

---

# 📊 Skill Dashboard

The system also generates a **visual dashboard** to show skill distribution.

Example output:

```
Python            ██████████ 80%
Pandas            █████████ 70%
Visualization     ███████ 60%
Machine Learning  █████ 40%
```

This helps learners understand which skills they already know and which areas need improvement.

---

# 📄 Project Documentation

Each generated project includes a **downloadable PDF** containing:

* project description
* required tools
* project architecture
* skill dashboard
* step-by-step implementation
* starter code

Users can download documentation for any generated project.

---

# 🏗 System Architecture

```
User Upload Material
        │
        ▼
Text Extraction
(PDF / DOCX)
        │
        ▼
AI Analysis (Groq LLM)
        │
        ├── Skill Extraction
        ├── Skill Dashboard
        ├── Project Generation
        └── Step-by-Step Build Plan
        │
        ▼
Streamlit Interface
        │
        ├── Project Details
        ├── Skill Visualization
        └── PDF Download
```

---

# 🧰 Tech Stack

Frontend

* Streamlit

Backend

* Python

AI Model

* Groq API (Llama 3)

Libraries

* PyPDF2
* python-docx
* pandas
* plotly
* reportlab

Deployment

* GitHub
* Streamlit Cloud

---

# 📁 Project Structure

```
ai-project-mentor/
│
├── app.py
├── ai_engine.py
├── file_parser.py
├── pdf_generator.py
├── requirements.txt
└── README.md
```

---

# 🛠 Installation

Clone the repository:

```
git clone https://github.com/yourusername/ai-project-mentor.git
cd ai-project-mentor
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```
streamlit run app.py
```

The application will start at:

```
http://localhost:8501
```

---

# ☁️ Deployment

You can deploy the project easily using **Streamlit Cloud**.

Steps:

1. Push the repository to GitHub
2. Connect the repository to Streamlit Cloud
3. Add your Groq API key in Streamlit secrets
4. Deploy the app

---

# 🚀 Future Improvements

* Support for YouTube and website learning materials
* Advanced skill analysis
* Personalized learning roadmap
* AI-based project evaluation
* Portfolio generation for learners

---

# 👨‍💻 Author

**Akash Bauri**
AI Engineer | Generative AI Developer

GitHub: https://github.com/akashbauri
LinkedIn: https://linkedin.com/in/akash-bauri
