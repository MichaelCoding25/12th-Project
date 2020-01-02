import sqlite3


conn = sqlite3.connect('members.db')

c = conn.cursor()


def create_member_id():
    c.execute("""CREATE TABLE members_id (
                name text,
                discriminator text
                )""")
    conn.commit()


def insert_member_id(name, discriminator):
    c.execute("INSERT INTO members_id VALUES (name, discriminator)")
    conn.commit()


conn.close()
