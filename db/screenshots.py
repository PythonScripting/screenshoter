import sqlite3
import time
import os

DB_NAME = os.environ["SCRSH_DB_NAME"]

def schedule(url, path, when=time.time(), status='new'):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    timestamp = time.time()
    retries = 0

    c.execute('INSERT INTO screenshots (url, status, scheduled, taken, path, retries) \
               VALUES (?, ?, ?, ?, ?, ?)', (url, status, when, timestamp, path, retries))

    conn.commit()
    c.close()

def find_upcoming():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    now = tuple([str(time.time())])

    upcoming_screenshots = c.execute('SELECT * FROM screenshots WHERE \
                                      (status == "new" AND scheduled < ?) OR \
                                      (status == "failed") AND (retries < 3)', now)
    upcoming_screenshots = list(upcoming_screenshots)

    c.close()
    return upcoming_screenshots

def done(ID):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('UPDATE screenshots SET status = "done" WHERE id == ?', ID)

    conn.commit()
    c.close()

def mark_completed_or_failed(id_outcome_retries):
    def transform(row):
        ID, return_code, retries = row
        retries += 1
        if return_code == 0:
            return ('done', retries, ID)
        else:
            return ('failed', retries, ID)

    status_retries_id = map(transform, id_outcome_retries)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.executemany('UPDATE screenshots SET status = ?, retries = ? WHERE id == ?', status_retries_id)

    conn.commit()
    c.close()

"""
CREATE TABLE urls (
    "url" TEXT NOT NULL,
    "added" REAL NOT NULL
, "status" TEXT);

CREATE TABLE screenshots (
    "id" INTEGER NOT NULL,
    "url" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "scheduled" REAL,
    "taken" REAL,
    "path" TEXT,
    "retries" INTEGER DEFAULT (0)
);
"""
