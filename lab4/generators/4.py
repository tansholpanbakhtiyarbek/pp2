a = int(input())
b = int(input())

def gen(a, b):
    for i in range(a, b + 1):
        yield i * i

for x in gen(a, b):
    print(x)