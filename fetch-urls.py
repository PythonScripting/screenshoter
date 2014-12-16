#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import time

from crawlers import timemk
import db


# Get newest urls from Time.mk
timemk_urls = timemk.newest_with_real_urls(pages=int(os.environ["SCRSH_TIME_MK_NEWEST_PAGES"]))

# Add unique urls to DB
db.urls.add_all_unique(timemk_urls)

# Schedule screenshots for new urls
new_urls = db.urls.find_new()

def gen_path():
    return os.path.join(os.environ["SCRSH_IMAGES_PATH"], str(random.random()) + '.jpg')

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
