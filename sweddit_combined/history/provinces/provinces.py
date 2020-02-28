import os
import regex as re

os.makedirs("new")

china_provinces = {}
fort_provinces = set()
china_file = open("china_provinces.txt", "r")
owner = None
for line in china_file:
    line = line.strip()
    if line.endswith("-fort"):
        line = line[:-5]
        fort_provinces.add(line)
    if re.match(r"\d+", line):
        china_provinces[line] = owner
    elif line:
        owner = line

for filename in os.listdir("."):
    province_id = filename.split("-")[0].strip()

    if province_id in china_provinces:
        old_file = open(filename, "r")
        new_text = ""
        owner = china_provinces[province_id]
        skip = False
        firstCore = True
        for line in old_file:
            if skip or line.startswith("fort_15th"):
                if "}" in line:
                    skip = False
            elif line.startswith("add_core"):
                if firstCore:
                    firstCore = False
                    new_text += "add_core = " + owner + "\n"
            elif line.startswith("owner"):
                new_text += "owner = " + owner + "\n"
            elif line.startswith("controller"):
                new_text += "controller = " + owner + "\n"
            elif re.match(r"\d{4}\.\d+\.\d+.*", line):
                if "}" not in line:
                    skip = True
            else:
                new_text += line
        if province_id in fort_provinces:
            new_text += "fort_15th = yes"
        new_file = open("new/" + filename, "w+")
        new_file.write(new_text.strip())
        old_file.close()
        new_file.close()

