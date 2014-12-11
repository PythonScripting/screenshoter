#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sqlite3
from multiprocessing.pool import ThreadPool as Pool

conn = sqlite3.connect('urls.sqlite')
c = conn.cursor()
rows = list(c.execute('SELECT * FROM urls WHERE (status == "new" OR status == "failed")'))

pool = Pool(5)

def take_screenshot(row):
    url, status, path, timestamp = row
    process = subprocess.Popen(['phantomjs', 'screenshot.js', url, path])
    process.wait()
    return (url, 'done', path)

print pool.map(take_screenshot, rows)
