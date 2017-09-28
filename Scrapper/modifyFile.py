import os


source = "./static/corpus/"
length = len(source)

files = os.listdir(source)

for fileName in files:
    contents = ""
    if fileName.endswith(".txt"):
        with open("./static/corpus/"+fileName, "r") as f:
            contents = f.read().split("\n")
            contents.pop(1)
        with open("./static/corpus/"+fileName, "w") as f:
            for line in contents:
                f.write(line)