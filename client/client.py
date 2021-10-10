##
#     Project: Django Remotes
# Description: A Django application to execute remote commands
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import argparse

from client.actions import (ACTION_AUTHENTICATE,
                            ACTION_GENERATE_KEYS,
                            ACTION_QUERY_STATUS,
                            ACTIONS)
from client.api import Api
from client.keys import Keys

from project import PRODUCT_NAME, VERSION


class Client(object):
    def __init__(self):
        self.options = None

    def get_command_line(self):
        parser = argparse.ArgumentParser(prog=f'{PRODUCT_NAME}')
        # Action argument
        parser.add_argument('--action',
                            type=str,
                            required=True,
                            choices=ACTIONS,
                            help='action to execute')
        # Version argument
        parser.add_argument('--version', '-V',
                            action='version',
                            version=f'{PRODUCT_NAME} v{VERSION}',
                            help='show version')
        # Key generation arguments
        group = parser.add_argument_group('Keys arguments')
        group.add_argument('--private_key',
                           type=str,
                           required=False,
                           help='private key filename')
        group.add_argument('--public_key',
                           type=str,
                           required=False,
                           help='public key filename')
        # Server arguments
        group = parser.add_argument_group('Server arguments')
        group.add_argument('--url',
                           type=str,
                           required=False,
                           help='server URL')
        group.add_argument('--token',
                           type=str,
                           required=False,
                           help='authentication token')
        # Process options
        options = parser.parse_args()
        self.options = options
        # Check needed extra arguments
        if options.action == ACTION_GENERATE_KEYS:
            if not options.private_key:
                parser.error('missing private_key argument')
            if not options.public_key:
                parser.error('missing public_key argument')
        elif options.action == ACTION_AUTHENTICATE:
            if not options.url:
                parser.error('missing URL argument')
            if not options.token:
                parser.error('missing token argument')
        elif options.action == ACTION_QUERY_STATUS:
            if not options.url:
                parser.error('missing URL argument')

    def process(self):
        status = -1
        result = None
        api = Api(url=self.options.url)
        headers = {}
        # Save token authorization if passed in the arguments
        if self.options.token:
            headers['Authorization'] = f'Token {self.options.token}'
        if self.options.action == ACTION_GENERATE_KEYS:
            # Generate private and public keys and save them in two files
            keys = Keys()
            keys.create_new_rsa_key(size=4096)
            keys.save_private_key(filename=self.options.private_key)
            keys.save_public_key(filename=self.options.public_key)
            status = 0
        elif self.options.action == ACTION_AUTHENTICATE:
            # Authenticate
            result = api.get(headers=headers)
            status = 0
        elif self.options.action == ACTION_QUERY_STATUS:
            # Query status
            result = api.get(headers=headers)
            status = 0
        return status, result
