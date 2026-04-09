from connect import get_connection

conn = get_connection()
cur = conn.cursor()

# search
cur.execute("SELECT * FROM search_contacts(%s)", ('Da',))
print("Search:")
for row in cur.fetchall():
    print(row)

# upsert
cur.execute("CALL upsert_contact(%s, %s)", ('Aida', '87012345678'))
conn.commit()

# pagination
cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (3, 0))
print("\nPagination:")
for row in cur.fetchall():
    print(row)

# delete
cur.execute("CALL delete_contact(%s)", ('Aida',))
conn.commit()

cur.close()
conn.close()