n = int(input())

def gen(n):
    while n >= 0:
        yield n
        n -= 1

for x in gen(n):
    print(x)