#!/usr/bin/env python

'''
File: gh_status.py
Author: Carno <carnophage at dobramama dot pl>
Description: Simple command line snippet to check GitHub status page
'''

from __future__ import print_function

import sys

try:
    import requests
except ImportError:
    print('Missing module: requests.')
    sys.exit(3)

GH_STATUS_API = 'https://status.github.com/api.json'

class GhStatus(object):
    """Methods for getting current GitHub status"""
    def __init__(self):
        api_request = requests.get(GH_STATUS_API)
        try:
            api_request.raise_for_status()
        except (requests.ConnectionError, requests.HTTPError, requests.Timeout,
                requests.TooManyRedirects) as err:
            print("Failed to get github status api [{0}]: {1}".format(err.errno,
                err.strerror))
            sys.exit(2)
        self.gh_api = api_request.json
        if not self.gh_api:
            print('Failed to decoded GitHub api json')
            sys.exit(2)
        self.gh_status = ''
        self.gh_last_msg = ''
        self.gh_last_msg_time = ''

    def get_status(self):
        """Get current github status"""
        status_request = requests.get(self.gh_api['status_url'])
        if not status_request.json:
            print('Failed to decode status json')
            sys.exit(2)
        self.gh_status = status_request.json['status']
        return self.gh_status

    def get_last_msg(self):
        """Get last message from GitHub status page"""
        last_msg_request = requests.get(self.gh_api['last_message_url'])
        last_msg = last_msg_request.json
        if not last_msg:
            print('Failed to decode last message json')
            sys.exit(2)
        self.gh_status = last_msg['status']
        self.gh_last_msg = last_msg['body']
        self.gh_last_msg_time = last_msg['created_on']
        return (self.gh_status, self.gh_last_msg, self.gh_last_msg_time)

def _main():
    """Dummy main function"""
    gh_status = GhStatus()
    current_status = gh_status.get_status()
    if current_status != 'good':
        print("GitHub has {0} issues :(\nLast update: {1} @{2}".format(gh_status.get_last_msg()))
        sys.exit(1)
    else:
        print('GitHub is good :)')
        sys.exit(0)

if __name__ == '__main__':
    _main()
