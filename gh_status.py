#!/usr/bin/env python

'''
File: gh_status.py
Author: Carno <carnophage at dobramama dot pl>
Description: Simple command line snippet to check github status page
'''

from __future__ import print_function

import sys
import json

try:
    import requests
except ImportError:
    print('Missing module: requests.')
    sys.exit(3)

if __name__ == '__main__':
    pass
