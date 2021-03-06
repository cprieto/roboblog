#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.
import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://cprieto.com'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'atom.xml'
CATEGORY_FEED_ATOM = ''

# Following items are often useful when publishing

GOOGLE_ANALYTICS = "UA-57001655-1"

FEED_DOMAIN = SITEURL

