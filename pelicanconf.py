#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os, sys

AUTHOR = u'Cristian Prieto'
SITENAME = u'IDisposable Thoughts'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Australia/Melbourne'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = os.path.join(os.path.dirname(os.path.realpath(__file__)), "newblog")
TYPOGRIFY = True

PLUGINS = ["neighbors"]

PYGMENTS_THEME = 'tomorrow'

MD_EXTENSIONS = ['codehilite(css_class=highlight,linenums=False)', 'extra', 'downheader']

sys.path.append('.')
import custom_filters

JINJA_FILTERS = {'all_but':custom_filters.all_but}

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}.html'

STATIC_PATHS = ['images', 'extras/robots.txt', 'extras/favicon.ico']
EXTRA_PATH_METADATA = {
    'extras/robots.txt': {'path': 'robots.txt'},
    'extras/favicon.ico': {'path': 'favicon.ico'}
}

YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/index.html'

ARCHIVES_SAVE_AS = 'posts/index.html'
TAGS_SAVE_AS = 'tag/index.html'
