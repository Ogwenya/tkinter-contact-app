import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, phone_number TEXT, email TEXT)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM contacts")
        data = self.cur.fetchall()
        return data

    def insert(self, first_name, last_name, phone_number, email):
        self.cur.execute("INSERT INTO contacts VALUES(Null, ?, ?, ?, ?)", (first_name, last_name, phone_number, email))
        self.conn.commit()

    def update(self, id, first_name, last_name, phone_number, email):
        self.cur.execute("UPDATE contacts SET first_name=?, last_name=?, phone_number=?, email=? WHERE id=?", (first_name, last_name, phone_number, email, id))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM contacts WHERE id=?", (id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

# dbase = Database('contacts.db')
# dbase.insert("John", "Doe", "+254703959541", "john@gmail.com")
# dbase.insert("Jane", "Does", "+254703955441", "jane@gmail.com")
# dbase.insert("Robinson", "Crusoe", "+254703955441", "robinsoncrusoe@gmail.com")