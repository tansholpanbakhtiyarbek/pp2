import json

data = {
    "name": "Dana",
    "age": 20
}

json_text = json.dumps(data)
print(json_text)