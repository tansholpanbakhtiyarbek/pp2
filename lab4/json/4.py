import json

with open("data/sample-data.json") as f:
    data = json.load(f)

print(len(data))

for x in data:
    print(x["name"])