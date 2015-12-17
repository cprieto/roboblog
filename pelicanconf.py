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

PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = ["neighbors"]

STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.png', 'figure']
PYGMENTS_THEME = 'colorful'

MD_EXTENSIONS = ['codehilite(css_class=highlight,linenums=False)', 'extra', 'downheader']

sys.path.append('.')
import custom_filters

JINJA_FILTERS = {'all_but':custom_filters.all_but}
