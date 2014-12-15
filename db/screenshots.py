import sqlite3
import time

def schedule(url, path, when=time.time(), status='new'):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    timestamp = time.time()

    c.execute('INSERT INTO screenshots (url, status, scheduled, taken, path) \
              VALUES (?, ?, ?, ?, ?)', (url, status, when, timestamp, path))

    conn.commit()
    c.close()

def find_upcoming():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    now = tuple([str(time.time())])

    upcoming_screenshots = c.execute('SELECT * FROM screenshots WHERE \
                                      (status == "new" AND scheduled < ?) OR \
                                      (status == "failed")', now)
    upcoming_screenshots = list(upcoming_screenshots)

    c.close()
    return upcoming_screenshots

def done(ID):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    c.execute('UPDATE screenshots SET status = "done" WHERE id == ?', ID)

    conn.commit()
    c.close()

def mark_completed_or_failed(id_status_pairs):
    def transform(pair):
        ID, return_code = pair
        if return_code == 0:
            return ('done', ID)
        else:
            return ('failed', ID)

    id_status_pairs = map(transform, id_status_pairs)

    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    c.executemany('UPDATE screenshots SET status = ? WHERE id == ?', id_status_pairs)

    conn.commit()
    c.close()
