n = int(input())

def even(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

print(",".join(map(str, even(n))))