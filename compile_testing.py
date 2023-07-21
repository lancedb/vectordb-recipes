import os, shutil, subprocess

try:
    os.mkdir("testing-folder")
except:
    pass

root = "./examples"

requirements = []
commands = []

# For each folder in the examples folder
for folders in os.listdir(root):
    folder = os.path.join(root, folders)
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            # If the file is a requirements.txt file, add it to the list of requirements
            if file.endswith("requirements.txt"):
                with open(os.path.join(folder, file), "r") as f:
                    requirements.extend(f.read().splitlines())
            # If the file is a python file, copy it to the testing folder
            if file.endswith(".py"):
                dup_name = folder.split("/")[-1] + ".py"
                shutil.copy(os.path.join(folder, file), os.path.join("./testing-folder", dup_name))
            # If the file is a jupyter notebook, convert it to a python file and copy it to the testing folder
            if file.endswith(".ipynb"):
                dup_name = folder.split("/")[-1] + "_IPYNB"
                with open("convert-ipynb.sh", "a+") as f:
                    f.write("jupyter nbconvert --output " + dup_name + " --output-dir=\"./testing-folder\" --RegexRemovePreprocessor.patterns=\"^[!%]\" --to python " + os.path.join(folder, file) + "\n")
            # If the file is a README.md file, add the dataset download commands to the list of commands
            if file.endswith("README.md"):
                with open(os.path.join(folder, file), "r") as f:
                    start = False
                    for line in f:
                        if line.startswith("```bash"):
                            start = True
                            continue
                        elif line.startswith("```"):
                            start = False
                        if start:
                            commands.append(line.strip())

# Add all requirements and remove lancedb for the repo build
with open("requirements.txt", "r") as f:
    requirements.extend(f.read().splitlines())

for i in requirements:
    if i == "lancedb":
        requirements.remove(i)

requirements.append("lancedb @ git+https://github.com/lancedb/lancedb.git#egg=subdir&subdirectory=python")

# Write the requirements and commands to files
with open("./testing-folder/joined-requirements.txt", "w") as f:
    for i in requirements:
        f.write(i + "\n")

with open('./testing-folder/commands.sh', 'w') as f:
    for i in commands:
        f.write(i + "\n")

print("Done!")