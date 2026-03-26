names = ["A", "B", "C"]
scores = [10, 20, 30]

for i, name in enumerate(names):
    print(i, name)

for name, score in zip(names, scores):
    print(name, score)

x = "5"
print(type(x))

x = int(x)
print(type(x))