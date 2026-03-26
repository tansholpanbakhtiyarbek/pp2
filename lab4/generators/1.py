n = int(input())

def gen(n):
    for i in range(n + 1):
        yield i * i

for x in gen(n):
    print(x)