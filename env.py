#!/usr/bin/env python

import os
from os.path import abspath, dirname, join

ROOT = abspath(dirname(__file__))
os.environ['TRANSFORMERS_CACHE'] = join(ROOT, 'model/cache')
