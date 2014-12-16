## Website screenshoter

Given a base of URLs, it makes screenshots.

# Installation steps on Ubuntu

```
git clone https://github.com/skopjehacklab/screenshoter.git
cd screenshoter/

sudo apt-get update
sudo apt-get install libxml2-dev libxslt-dev python-dev
pip install lxml --user

pip install cssselect --user

sudo apt-get install sqlite3
touch db.sqlite

sqlite3
> .open db.sqlite
> .read db/initdb.sql
> ^D

mkdir images

# install phantomjs ..
```

To add new urls:

`soruce config.sh && python fetch-urls.py`

To take screenshots for scheduled urls:

`source config.sh && python take-screenshots.py`