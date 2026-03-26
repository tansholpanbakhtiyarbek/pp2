# copy_delete_files.py

import shutil
import os

shutil.copy("test.txt", "backup.txt")

if os.path.exists("backup.txt"):
    os.remove("backup.txt")