from datetime import datetime

dt = datetime.now()
dt = dt.replace(microsecond=0)

print(dt)