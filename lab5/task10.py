import re

text = "camelCaseString"
pattern = r"([A-Z])"

result = re.sub(pattern, r"_\1", text).lower()
print(result)