import json

data = {
    "city": "Almaty",
    "year": 2026
}

with open("data/output.json", "w") as f:
    json.dump(data, f)

print("written")