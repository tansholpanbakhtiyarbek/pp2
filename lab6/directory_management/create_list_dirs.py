import os

os.makedirs("my_folder/subfolder", exist_ok=True)

for item in os.listdir():
    print(item)