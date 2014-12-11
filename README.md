## Website screenshoter

Given a base of URLs, it makes screenshots.

## To run

0. Git clone this repo
1. Install PhantomJS 1.9+
2. Install Python 2.7
3. Install python modules: lxml, requests
4. Make dir 'images/'
5. Create database 'urls.sqlite'

To add new urls:

`python cralwers/time.py`

To take screenshots for all urls:

`python screenshot.py`