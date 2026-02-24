from datetime import datetime

fmt = "%Y-%m-%d %H:%M:%S"

d1 = input()
d2 = input()

a = datetime.strptime(d1, fmt)
b = datetime.strptime(d2, fmt)

print(int(abs((b - a).total_seconds())))