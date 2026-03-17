import re

text = "abbb"
pattern = r"^ab*$"

if re.match(pattern, text):
    print("Matched")
else:
    print("Not matched")