import re

text = "hello_world my_variable test_string"
pattern = r"\b[a-z]+_[a-z]+\b"

result = re.findall(pattern, text)
print(result)