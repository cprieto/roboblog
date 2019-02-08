#!/usr/bin/env python
from __future__ import unicode_literals
import os, sys

AUTHOR = u'Cristian Prieto'
SITENAME = u'IDisposable Thoughts'
SITEURL = ''

PATH = os.path.join(os.getcwd(), 'content')

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = u'en'
DEFAULT_DATE = 'fs'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing

THEME = os.path.join(os.path.dirname(os.path.realpath(__file__)), "theme")
TYPOGRIFY = True

# Readtime is giving issues
PLUGINS = ['neighbors','readtime','extended_sitemap','pelican_jsmath',]

PYGMENTS_THEME = 'tomorrow'

MARKDOWN = {
    'extensions': ['fenced_code', 'mdx_headdown', 'extra', 'mdx_notebook'],
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight', 'linenums': False},
        'markdown.extensions.extra': {},
        'mdx_headdown': { 'offset': 2, },
        'mdx_notebook': {'label_text': 'Out[*]:'},
        'markdown.extensions.admonition': {},
    },
    'output_format': 'html5'
}

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

OUTPUT_PATH = 'output/'
DIRECT_TEMPLATES = ['index', 'archives', 'tags']

AUTHOR_URL = ''
AUTHOR_SAVE_AS = ''

USE_FOLDER_AS_CATEGORY = False
CATEGORY_URL = ''
CATEGORY_SAVE_AS = ''

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
