import re

text = "Hello world Python Java CODE"
pattern = r"\b[A-Z][a-z]+\b"

result = re.findall(pattern, text)
print(result)