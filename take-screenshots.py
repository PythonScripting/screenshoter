#!/usr/bin/env python
# -*- coding: utf-8 -*-

from screenshooter import capture_all
import db

def id_url_path_retries(rows):
    arr = []
    for row in rows:
        ID, url, status, scheduled, taken, path, retries = row
        extracted_data = (ID, url, path, retries)
        arr.append(extracted_data)
    return arr

# Find scheduled screenshot entries
upcoming = db.screenshots.find_upcoming()

# Take (id, url, path, retries) out of every row
rows = id_url_path_retries(upcoming)

# Capture (run phantom) and save to file, return outcomes
id_outcome_retries = capture_all(rows)

# Update DB for every outcome
db.screenshots.mark_completed_or_failed(id_outcome_retries)
