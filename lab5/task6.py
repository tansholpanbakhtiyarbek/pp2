import re

text = "Hello, world. Python regex"
pattern = r"[ ,.]"

result = re.sub(pattern, ":", text)
print(result)