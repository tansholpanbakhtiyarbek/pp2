import re

text = "abbb"
pattern = r"^ab{2,3}$"

if re.match(pattern, text):
    print("Matched")
else:
    print("Not matched")