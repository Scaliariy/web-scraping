import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute("select * from events where date='2088.10.15'")
print(cursor.fetchall())

cursor.execute("select band,date from events where date='2088.10.15'")
print(cursor.fetchall())

# new_rows = [('Cats', 'Cats City', '2088.10.17'), ('Dogs', 'Dogs City', '2088.10.17')]
# cursor.executemany("insert into events values(?,?,?)", new_rows)
# connection.commit()

cursor.execute("select * from events")
print(cursor.fetchall())
