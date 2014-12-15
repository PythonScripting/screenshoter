#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sqlite3
from multiprocessing.pool import ThreadPool as Pool
import time
import random

from screenshooter import capture_all
from crawlers import timemk
import db

def id_url_path_triplets(rows):
    url_path_pairs = []
    for row in rows:
        print row
        ID, url, status, scheduled, taken, path = row
        triplet = (ID, url, path)
        url_path_pairs.append(triplet)
    return url_path_pairs

# Get newest urls from Time.mk
timemk_urls = timemk.newest_with_real_urls(pages=1)

# Add unique urls to DB
db.urls.add_all_unique(timemk_urls)

# Schedule screenshots for new urls
new_urls = db.urls.find_new()

def gen_path():
    return 'images/' + str(random.random()) + '.jpg' # todo: path join

for row in new_urls:
    url, added, status = row

    now = time.time() # seconds since unix epoch
    one_hour = 60 * 60
    one_day = one_hour * 24
    one_week = one_day * 7
    one_month = one_week * 4

    db.screenshots.schedule(url, gen_path(), now)
    db.screenshots.schedule(url, gen_path(), now + one_hour)
    db.screenshots.schedule(url, gen_path(), now + one_day)
    db.screenshots.schedule(url, gen_path(), now + one_week)
    db.screenshots.schedule(url, gen_path(), now + one_month)

db.urls.mark_completed(new_urls)

# Find scheduled screenshot entries
upcoming = db.screenshots.find_upcoming()

# Make (id, url, path) triplets out of every row
triplets = id_url_path_triplets(upcoming)

# Capture (run phantom) and save to file, return outcomes
id_outcome_pairs = capture_all(triplets)

# Update DB for every outcome
db.screenshots.mark_completed_or_failed(id_outcome_pairs)

# Print outcomes
print 'done'
