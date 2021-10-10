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
                            ACTION_DISCOVER,
                            ACTION_GENERATE_KEYS,
                            ACTION_STATUS,
                            ACTIONS)
from client.api import Api
from client.keys import Keys
from client.settings import (Settings,
                             OPTION_PRIVATE_KEY,
                             OPTION_PUBLIC_KEY,
                             OPTION_TOKEN,
                             SECTION_ENDPOINTS,
                             SECTION_HOST,
                             SECTION_SERVER)

from project import PRODUCT_NAME, VERSION

from remotes.constants import ENDPOINTS, SERVER_URL


class Client(object):
    def __init__(self):
        self.options = None
        self.settings = None

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
        # Settings argument
        parser.add_argument('--settings', '-S',
                            type=str,
                            required=False,
                            help='settings filename')
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
        if options.action == ACTION_STATUS:
            if not options.url:
                parser.error('missing URL argument')
            if not options.settings:
                parser.error('missing settings argument')
        elif options.action == ACTION_DISCOVER:
            if not options.settings:
                parser.error('missing settings argument')
        elif options.action == ACTION_GENERATE_KEYS:
            if not options.settings:
                parser.error('missing settings argument')
            if not options.private_key:
                parser.error('missing private_key argument')
            if not options.public_key:
                parser.error('missing public_key argument')
        elif options.action == ACTION_AUTHENTICATE:
            if not options.settings:
                parser.error('missing settings argument')
            if not options.token:
                parser.error('missing token argument')

    def process(self):
        status = -1
        result = None
        api = Api(url=self.options.url)
        headers = {}
        # Save token authorization if passed in the arguments
        if self.options.token:
            headers['Authorization'] = f'Token {self.options.token}'
        if self.options.action == ACTION_STATUS:
            # Get status
            result = api.get(headers=headers)
            status = 0
            # Update settings
            self.settings.set_value(section=SECTION_SERVER,
                                    option=SERVER_URL,
                                    value=result[SERVER_URL])
            self.settings.set_value(section=SECTION_ENDPOINTS,
                                    option=ACTION_DISCOVER,
                                    value=result[ACTION_DISCOVER])
        elif self.options.action == ACTION_DISCOVER:
            # Discover services URLS
            api.url = self.settings.build_url(
                url=self.settings.get_value(section=SECTION_ENDPOINTS,
                                            option=ACTION_DISCOVER))
            result = api.get(headers=headers)
            status = 0
            # Update settings
            for endpoint in result[ENDPOINTS]:
                self.settings.set_value(section=SECTION_ENDPOINTS,
                                        option=endpoint,
                                        value=result[ENDPOINTS][endpoint])
        elif self.options.action == ACTION_GENERATE_KEYS:
            # Generate private and public keys and save them in two files
            keys = Keys()
            keys.create_new_rsa_key(size=4096)
            keys.save_private_key(filename=self.options.private_key)
            keys.save_public_key(filename=self.options.public_key)
            status = 0
            # Update settings
            self.settings.set_value(section=SECTION_HOST,
                                    option=OPTION_PRIVATE_KEY,
                                    value=self.options.private_key)
            self.settings.set_value(section=SECTION_HOST,
                                    option=OPTION_PUBLIC_KEY,
                                    value=self.options.public_key)
        elif self.options.action == ACTION_AUTHENTICATE:
            # Authenticate
            api.url = self.settings.build_url(
                url=self.settings.get_value(section=SECTION_ENDPOINTS,
                                            option=ACTION_AUTHENTICATE))
            result = api.get(headers=headers)
            status = 0
            # Update settings
            self.settings.set_value(section=SECTION_HOST,
                                    option=OPTION_TOKEN,
                                    value=self.options.token)
        return status, result

    def load(self):
        """
        Load settings
        :return: None
        """
        self.settings = Settings()
        if self.options.settings:
            self.settings.load(self.options.settings)

    def save(self):
        """
        Save settings
        :return: None
        """
        if self.options.settings:
            self.settings.save(self.options.settings)
