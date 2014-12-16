from lxml import etree
from lxml.cssselect import CSSSelector
import requests as r
from multiprocessing.pool import ThreadPool as Pool
import sqlite3
import time
import random
import os

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

def newest_with_real_urls(pages=10):
    pool = Pool(int(os.environ["SCRSH_TIME_MK_THREAD_POOL"]))
    return pool.map(real_url, newest(pages))
