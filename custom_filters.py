# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest

'''
Custom Jinja2 functions for my blog
'''

__version__ = '1.0.0'

def all_but(items, not_this):
    return [item for item in items if item != not_this]
