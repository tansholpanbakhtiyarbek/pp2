from functools import reduce

numbers = [1, 2, 3, 4, 5]

result = list(map(lambda x: x * 2, numbers))
print(result)

even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)

total = reduce(lambda x, y: x + y, numbers)
print(total)