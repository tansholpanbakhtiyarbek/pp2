import csv
import json
from connect import get_connection


# ===================== RUN SQL FILE =====================
def run_sql_file(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        sql = file.read()
        cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()

    print(f"{filename} executed successfully.")


# ===================== ADD CONTACT =====================
def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group (Family/Work/Friend/Other): ")
    phone = input("Phone: ")
    phone_type = input("Phone type (home/work/mobile): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL upsert_contact(%s, %s, %s, %s, %s, %s)",
        (name, email, birthday, group, phone, phone_type)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added successfully.")


# ===================== ADD PHONE =====================
def add_phone():
    name = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Phone type (home/work/mobile): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL add_phone(%s, %s, %s)",
        (name, phone, phone_type)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added successfully.")


# ===================== MOVE TO GROUP =====================
def move_to_group():
    name = input("Contact name: ")
    group = input("New group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL move_to_group(%s, %s)",
        (name, group)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved successfully.")


# ===================== SHOW ALL CONTACTS =====================
def show_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.name;
    """)

    rows = cur.fetchall()

    print("\n--- CONTACTS ---")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


# ===================== SEARCH CONTACTS =====================
def search_contacts():
    query = input("Search by name/email/phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()

    print("\n--- SEARCH RESULTS ---")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


# ===================== FILTER BY GROUP =====================
def filter_by_group():
    group = input("Group name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name = %s
        ORDER BY c.name;
    """, (group,))

    rows = cur.fetchall()

    print("\n--- GROUP CONTACTS ---")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


# ===================== SORT CONTACTS =====================
def sort_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")

    choice = input("Choose: ")

    if choice == "1":
        order_by = "c.name"
    elif choice == "2":
        order_by = "c.birthday"
    elif choice == "3":
        order_by = "c.date_added"
    else:
        print("Wrong choice.")
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY {order_by};
    """)

    rows = cur.fetchall()

    print("\n--- SORTED CONTACTS ---")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


# ===================== PAGINATION =====================
def paginated_contacts():
    limit = 3
    offset = 0

    while True:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, offset))
        rows = cur.fetchall()

        print("\n--- PAGE ---")
        for row in rows:
            print(row)

        cur.close()
        conn.close()

        command = input("next / prev / quit: ")

        if command == "next":
            offset += limit

        elif command == "prev":
            offset = max(0, offset - limit)

        elif command == "quit":
            break


# ===================== UPDATE CONTACT =====================
def update_contact():
    name = input("Contact name to update: ")
    new_email = input("New email: ")
    new_birthday = input("New birthday (YYYY-MM-DD): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE contacts
        SET email = %s,
            birthday = %s
        WHERE name = %s;
    """, (new_email, new_birthday, name))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact updated successfully.")


# ===================== DELETE CONTACT =====================
def delete_contact():
    value = input("Enter name or phone to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact deleted successfully.")


# ===================== IMPORT FROM CSV =====================
def import_csv():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cur.execute(
                "CALL upsert_contact(%s, %s, %s, %s, %s, %s)",
                (
                    row["name"],
                    row["email"],
                    row["birthday"],
                    row["group"],
                    row["phone"],
                    row["phone_type"]
                )
            )

    conn.commit()
    cur.close()
    conn.close()

    print("CSV imported successfully.")


# ===================== EXPORT TO JSON =====================
def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.name;
    """)

    contacts = cur.fetchall()
    data = []

    for contact in contacts:
        contact_id, name, email, birthday, group = contact

        cur.execute("""
            SELECT phone, type
            FROM phones
            WHERE contact_id = %s;
        """, (contact_id,))

        phones = cur.fetchall()

        data.append({
            "name": name,
            "email": email,
            "birthday": str(birthday),
            "group": group,
            "phones": [
                {"phone": phone, "type": phone_type}
                for phone, phone_type in phones
            ]
        })

    with open("contacts_export.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    cur.close()
    conn.close()

    print("Contacts exported to contacts_export.json")


# ===================== IMPORT FROM JSON =====================
def import_json():
    with open("contacts.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    for contact in data:
        name = contact["name"]

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()

        if existing:
            choice = input(f"{name} already exists. skip/overwrite: ")

            if choice == "skip":
                continue

            elif choice == "overwrite":
                cur.execute("CALL delete_contact(%s)", (name,))

        phones = contact["phones"]

        for phone_item in phones:
            cur.execute(
                "CALL upsert_contact(%s, %s, %s, %s, %s, %s)",
                (
                    contact["name"],
                    contact["email"],
                    contact["birthday"],
                    contact["group"],
                    phone_item["phone"],
                    phone_item["type"]
                )
            )

    conn.commit()
    cur.close()
    conn.close()

    print("JSON imported successfully.")


# ===================== MAIN MENU =====================
def main():
    while True:
        print("\n========== PHONEBOOK MENU ==========")
        print("1. Run schema.sql")
        print("2. Run procedures.sql")
        print("3. Add contact")
        print("4. Add phone to contact")
        print("5. Move contact to group")
        print("6. Show contacts")
        print("7. Search contacts")
        print("8. Filter by group")
        print("9. Sort contacts")
        print("10. Paginated contacts")
        print("11. Update contact")
        print("12. Delete contact")
        print("13. Import CSV")
        print("14. Export JSON")
        print("15. Import JSON")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            run_sql_file("schema.sql")
        elif choice == "2":
            run_sql_file("procedures.sql")
        elif choice == "3":
            add_contact()
        elif choice == "4":
            add_phone()
        elif choice == "5":
            move_to_group()
        elif choice == "6":
            show_contacts()
        elif choice == "7":
            search_contacts()
        elif choice == "8":
            filter_by_group()
        elif choice == "9":
            sort_contacts()
        elif choice == "10":
            paginated_contacts()
        elif choice == "11":
            update_contact()
        elif choice == "12":
            delete_contact()
        elif choice == "13":
            import_csv()
        elif choice == "14":
            export_json()
        elif choice == "15":
            import_json()
        elif choice == "0":
            break
        else:
            print("Wrong choice.")


if __name__ == "__main__":
    main()