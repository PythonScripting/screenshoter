#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sqlite3
from multiprocessing.pool import ThreadPool as Pool
import time

conn = sqlite3.connect('urls.sqlite')
c = conn.cursor()
rows = list(c.execute('SELECT * FROM urls WHERE (status == "new" OR status == "failed")'))

pool = Pool(5)

def take_screenshot(row):
    url, status, path, timestamp = row
    url = real_url(url)
    timestamp = time.time()
    process = subprocess.Popen(['phantomjs', 'screenshot.js', url, path])
    process.wait()
    if process.returncode == 0:
        return (url, 'done', path, timestamp)
    else:
        return (url, 'failed', path, timestamp)

updated_rows = pool.map(take_screenshot, rows)
conn.executemany('INSERT OR REPLACE INTO urls VALUES (?, ?, ?, ?)', updated_rows);

conn.commit()
c.close()
