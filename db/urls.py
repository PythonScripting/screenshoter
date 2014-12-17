import sqlite3
import time
import os

DB_NAME = os.environ["SCRSH_DB_NAME"]

def add_unique(url):
    conn = sqlite3.connect()
    c = conn.cursor()

    timestamp = time.time()
    c.execute('INSERT OR IGNORE INTO urls VALUES (?, ?, ?)', url, timestamp, 'new')

    conn.commit()
    c.close()

def add_all_unique(urls):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    url_timestamp_status_triplets = map(lambda url: (url, time.time(), 'new'), urls)
    c.executemany('INSERT OR IGNORE INTO urls VALUES (?, ?, ?)', url_timestamp_status_triplets)

    conn.commit()
    c.close()

def find_new():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    new_urls = list(c.execute('SELECT * FROM urls WHERE status == "new"'))

    c.close()
    return new_urls

def mark_completed(urls):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # extract just the url
    urls = map(lambda url: (url[0],), urls)

    c.executemany('UPDATE urls SET status = "done" WHERE url == ?', urls)

    conn.commit()
    c.close()
