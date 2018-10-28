#!/usr/bin/env python3

"""Description: Simple command line snippet to check GitHub status page."""

import json
import sys
from logzero import logger

try:
    import requests
except ImportError:
    print('Missing module: requests.')
    sys.exit(3)

GH_STATUS_API = 'https://status.github.com/api.json'


class GhStatus:
    """Methods for getting current GitHub status."""

    def __init__(self):
        """Initialize defaults."""
        try:
            api_request = requests.get(GH_STATUS_API)
            api_request.raise_for_status()
        except requests.exceptions.RequestException:
            logger.error('Failed to get github:status api')
            sys.exit(2)
        try:
            self.gh_api = api_request.json()
        except json.JSONDecodeError:
            logger.error('Failed to decode Github api json')
            sys.exit(2)
        self.gh_status = ''
        self.gh_last_msg = ''
        self.gh_last_msg_time = ''

    def get_status(self):
        """Get current github status."""
        try:
            status_request = requests.get(self.gh_api['status_url'])
        except requests.exceptions.RequestException:
            logger.error('Failed to get status_url json')
            sys.exit(2)
        try:
            self.gh_status = status_request.json()['status']
        except json.JSONDecodeError:
            logger.error('Failed to decode status json')
            sys.exit(2)
        return self.gh_status

    def get_last_msg(self):
        """Get last message from GitHub status page."""
        try:
            last_msg_request = requests.get(self.gh_api['last_message_url'])
        except requests.exceptions.RequestException:
            logger.error('Failed to get last_message_url json')
            sys.exit(2)
        try:
            last_msg = last_msg_request.json()
        except json.JSONDecodeError:
            logger.error('Failed to decode last message json')
            sys.exit(2)
        self.gh_status = last_msg['status']
        self.gh_last_msg = last_msg['body']
        self.gh_last_msg_time = last_msg['created_on']
        return (self.gh_status, self.gh_last_msg_time, self.gh_last_msg)


def _main():
    """Perform current status check."""
    gh_status = GhStatus()
    current_status = gh_status.get_status()
    if current_status != 'good':
        logger.warning('GitHub has %s issues 8^( Last update @%s: %s)', *gh_status.get_last_msg())
        sys.exit(1)
    else:
        logger.info('GitHub is good 8^)')
        sys.exit(0)


if __name__ == '__main__':
    _main()
