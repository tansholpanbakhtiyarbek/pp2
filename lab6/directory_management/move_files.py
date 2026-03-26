import shutil
import os

os.makedirs("move_here", exist_ok=True)

if os.path.exists("test.txt"):
    shutil.move("test.txt", "move_here/test.txt")