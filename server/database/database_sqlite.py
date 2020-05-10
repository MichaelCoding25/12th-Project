# Handles the database
import sqlite3
from start import CURRENT_DIR as CD

MEMBERS_DATABASE_DIRECTORY = CD + '/server/database/members.db'


def create_members_info_table():
    """
    Creates the members_info table if one does not exist in the db file and inputs all needed columns.
    :return:
    """
    conn = sqlite3.connect(MEMBERS_DATABASE_DIRECTORY)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS members_info (
                    mem_id      TEXT    NOT NULL,
                    date_time    INTEGER NOT NULL,
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
    conn = sqlite3.connect(MEMBERS_DATABASE_DIRECTORY)
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
    conn = sqlite3.connect(MEMBERS_DATABASE_DIRECTORY)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS statuses (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    st_name TEXT    NOT NULL
                );         
    """)
    conn.commit()
    c.execute("SELECT id FROM statuses")
    if len(c.fetchall()) == 0:
        c.execute("""INSERT INTO statuses (id, st_name)
                     VALUES 
                     (1 , 'offline'),
                     (2 , 'online'),
                     (3 , 'idle'),
                     (4 , 'dnd');
        """)
        conn.commit()
    conn.close()


def create_perms_tables():
    conn = sqlite3.connect(MEMBERS_DATABASE_DIRECTORY)
    c = conn.cursor()
    c.execute(f"""CREATE TABLE role_perms (
                d_role            TEXT    UNIQUE
                                          NOT NULL,
                d_can_view_self   BOOLEAN NOT NULL,
                d_can_view_others BOOLEAN NOT NULL,
                d_can_view_server BOOLEAN NOT NULL,
                d_can_view_roles  BOOLEAN NOT NULL,
                d_can_view_perms  BOOLEAN NOT NULL
            );
    """)
    conn.commit()
    c.execute("""INSERT INTO role_perms
                 VALUES 
                 ('d_owner', 1, 1, 1, 1, 1),
                 ('d_admin', 1, 1, 0, 1, 1),
                 ('d_mod', 1, 1, 0, 1, 0),
                 ('d_mem', 1, 0, 0, 0, 0);
    """)
    conn.commit()
    conn.close()