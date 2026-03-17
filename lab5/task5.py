import re

text = "axxxb"
pattern = r"^a.*b$"

if re.match(pattern, text):
    print("Matched")
else:
    print("Not matched")