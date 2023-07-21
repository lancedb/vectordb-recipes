import os, shutil

os.mkdir("testing-folder")

requirements = []
for root, dirs, files in os.walk(".\examples"):
    for i, file in enumerate(files):
        if file.endswith("requirements.txt"):
            with open(os.path.join(root, file), "r") as f:
                requirements.append(f.read().splitlines())
        if file.endswith(".py"):
            dup_name = root.split("\\")[-1] + ".py"
            shutil.copy(os.path.join(root, file), os.path.join("testing-folder", dup_name))

requirements = [item for sublist in requirements for item in sublist]

for i in requirements:
    if i == "lancedb":
        requirements.remove(i)

with open("joined-requirements.txt", "w") as f:
    for i in requirements:
        f.write(i + "\n")

