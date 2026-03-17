import re

text = "SplitThisStringAtUppercaseLetters"
pattern = r"(?=[A-Z])"

result = re.split(pattern, text)
result = [word for word in result if word]

print(result)