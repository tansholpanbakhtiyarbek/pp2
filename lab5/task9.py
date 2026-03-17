import re

text = "InsertSpacesBetweenWords"
pattern = r"([A-Z])"

result = re.sub(pattern, r" \1", text).strip()
print(result)