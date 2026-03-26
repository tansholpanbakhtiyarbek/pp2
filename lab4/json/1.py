import json

text = '{"name":"Ali","age":19}'
data = json.loads(text)

print(data["name"])
print(data["age"])