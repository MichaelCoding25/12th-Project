# Handles the database
import sqlite3


def create_members_info_table():
    """
    Creates the members_info table if one does not exist in the db file and inputs all needed columns.
    :return:
    """
    conn = sqlite3.connect('members.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS members_info (
                    mem_id      TEXT    NOT NULL,
                    datetime    INTEGER NOT NULL,
                    status_id   INTEGER,
                    activity_id INTEGER
                );
    """)
    conn.commit()
    conn.close()


def create_activities_table():
    """
    Creates the activities table if one does not exist in the db file and inputs all needed columns.
    :return:
    """
    conn = sqlite3.connect('members.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS activities (
                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    act_name TEXT    NOT NULL
                );
    """)
    conn.commit()
    conn.close()


def create_statuses_table():
    """
    Creates the statuses table if one does not exist in the db file and inputs all needed columns.
    :return:
    """
    conn = sqlite3.connect('members.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS statuses (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    st_name TEXT    NOT NULL
                );         
    """)
    conn.commit()
    c.execute("SELECT id FROM statuses")
    if len(c.fetchall()) is 0:
        c.execute("""INSERT INTO statuses (id, st_name)
                     VALUES 
                     (1 , 'offline'),
                     (2 , 'online'),
                     (3 , 'idle'),
                     (4 , 'dnd');
        """)
        conn.commit()
    conn.close()
