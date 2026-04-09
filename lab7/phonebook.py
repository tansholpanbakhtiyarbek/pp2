from connect import get_connection
import csv

conn = get_connection()
cur = conn.cursor()
with open("contacts.csv", newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        cur.execute(
            "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
            (row[0], row[1])
        )
conn.commit()
# INSERT
name = input("Enter name: ")
phone = input("Enter phone: ")

cur.execute(
    "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
    (name, phone)
)
conn.commit()

# UPDATE
update_name = input("Enter name to update: ")
new_phone = input("Enter new phone: ")

cur.execute(
    "UPDATE phonebook SET phone = %s WHERE username = %s",
    (new_phone, update_name)
)
conn.commit()

# DELETE
delete_name = input("Enter name to delete: ")

cur.execute(
    "DELETE FROM phonebook WHERE username = %s",
    (delete_name,)
)
conn.commit()

# FILTER
search = input("Enter name to search: ")

cur.execute(
    "SELECT * FROM phonebook WHERE username LIKE %s",
    ("%" + search + "%",)
)

rows = cur.fetchall()
for row in rows:
    print(row)

cur.close()
conn.close()