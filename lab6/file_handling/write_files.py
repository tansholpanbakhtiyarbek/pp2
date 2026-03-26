# write_files.py

with open("test.txt", "w") as f:
    f.write("Hello\n")
    f.write("This is a test file\n")

with open("test.txt", "a") as f:
    f.write("New line added\n")