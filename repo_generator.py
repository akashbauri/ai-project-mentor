import os
import zipfile


def create_repo_zip(project_name):

    folder = project_name.replace(" ", "_").lower()

    os.makedirs(folder + "/src", exist_ok=True)
    os.makedirs(folder + "/data", exist_ok=True)

    readme = f"""
# {project_name}

Generated using AI Project Mentor

Author: Akash Bauri
"""

    with open(f"{folder}/README.md", "w") as f:
        f.write(readme)

    with open(f"{folder}/requirements.txt", "w") as f:
        f.write("pandas\nscikit-learn\nmatplotlib\n")

    with open(f"{folder}/src/main.py", "w") as f:
        f.write("print('Project started successfully')")

    zip_name = folder + ".zip"

    with zipfile.ZipFile(zip_name, "w") as zipf:

        for root, dirs, files in os.walk(folder):

            for file in files:

                filepath = os.path.join(root, file)

                zipf.write(filepath)

    return zip_name
