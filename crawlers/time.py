from lxml import etree
from lxml.cssselect import CSSSelector
import requests as r
import requests as r

def find(selector, content):
    """ Select elements from the DOM, like in jQuery.

    Example:
    >>> find('h1 a#link', '<h1><a id="link">Something</a></h1>')
    """

    # Find should work on both HTML strings
    # and parsed lxml nodes.
    if type(content) == str:
        content = etree.HTML(content)

    return CSSSelector(selector)(content)

def find_one(selector, content):
    """ Same as `find` just for one element.
    """
    elements = find(selector, content)
    return elements[0]

def real_url(url):
    """ Returns the URL after all the redirects.
    """
    print url
    return r.get(url).url

def newest(pages=10):
    """ Finds the latest news on Time.mk
    """
    pages = min(pages, 10)
    for page in xrange(1, pages + 1):
        response = r.get('http://www.time.mk/n/all/%s' % page)
        paragraphs = find('div.cluster', response.text.encode('utf8'))
        for p in paragraphs:
            yield 'http://time.mk/' + find_one('h1 a', p).get('href')

import sqlite3
import time
import random

urls_to_add = []
for url in newest():
    # todo: path join
    record = url, 'new', 'images/' + str(random.random()) + '.png', str(time.time())
    urls_to_add.append(record)

print urls_to_add

conn = sqlite3.connect('urls.sqlite')
c = conn.cursor()
rows = c.executemany('INSERT OR IGNORE INTO urls VALUES (?, ?, ?, ?)', urls_to_add)

conn.commit()
c.close()
