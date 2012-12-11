#!/usr/bin/env python

'''
File: gh-status.py
Author: Carno <carnophage at dobramama dot pl>
Description: Simple command line snippet to check github status
'''

from __future__ import print_function

import sys
import json

try:
    import requests
except ImportError:
    print('Needed module: requests not available! Please install it and try again')
    sys.exit(3)

if __name__ == '__main__':
    pass
