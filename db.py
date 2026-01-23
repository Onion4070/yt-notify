import os
import sqlite3
import time
import random, string


def randomname(n):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def insert_data(db_name, channel_id, topic_url, callback_url, lease_seconds, subscribed_at, expires_at, status):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO subscribe(
            channel_id, 
            topic_url, 
            callback_url, 
            lease_seconds, 
            subscribed_at, 
            expires_at, 
            status
        )
        values(?, ?, ?, ?, ?, ?, ?)
    """, (
        channel_id, 
        topic_url, 
        callback_url, 
        lease_seconds, 
        subscribed_at, 
        expires_at, 
        status
    ))

    conn.commit()
    cur.close()


def print_table(db_name: str, table_name: str):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()


def create_db(db_name: str):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE subscribe(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 

            channel_id TEXT NOT NULL UNIQUE, 
            topic_url TEXT NOT NULL UNIQUE, 
            callback_url TEXT NOT NULL, 

            lease_seconds INTEGER NOT NULL, 
            subscribed_at INTEGER NOT NULL, 
            expires_at INTEGER, 
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def init(db_name: str):
    if not os.path.isfile(db_name):
        create_db(db_name)


if __name__ == '__main__':
    db_name = 'test.db'
    init(db_name)

    channel_id = randomname(8)
    topic_url = f'https://youtube.com/user/{channel_id}'
    callback_url = 'https://notify.youtube.com/callback'
    lease_seconds = 86400
    subscribed_at = int(time.time())
    expires_at = subscribed_at + lease_seconds
    status = 'subscried'
    insert_data(db_name, channel_id, topic_url, callback_url, lease_seconds, subscribed_at, expires_at, status)
    print_table(db_name, 'subscribe')
