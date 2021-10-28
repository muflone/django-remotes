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
import os
import subprocess
import sys
import tempfile

from encryption.rsa_key import RsaKey

from project import PRODUCT_NAME, VERSION

from remotes.client.actions import (ACTION_COMMAND_GET,
                                    ACTION_COMMANDS_LIST,
                                    ACTION_DISCOVER,
                                    ACTION_GENERATE_KEYS,
                                    ACTION_STATUS,
                                    ACTION_HOST_REGISTER,
                                    ACTION_HOST_VERIFY,
                                    ACTIONS)
from remotes.client.api import Api
from remotes.client.settings import (Settings,
                                     OPTION_PRIVATE_KEY,
                                     OPTION_PUBLIC_KEY,
                                     OPTION_TOKEN,
                                     SECTION_ENDPOINTS,
                                     SECTION_HOST,
                                     SECTION_SERVER)
from remotes.constants import (ENCRYPTED_FIELD,
                               ENDPOINTS_FIELD,
                               MESSAGE_FIELD,
                               PUBLIC_KEY_FIELD,
                               SERVER_URL,
                               STATUS_FIELD,
                               STATUS_ERROR,
                               STATUS_OK,
                               UUID_FIELD)


class Client(object):
    def __init__(self):
        self.options = None
        self.settings = None
        self.key = None

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
                            required=True,
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
        # Command arguments
        group = parser.add_argument_group('Command')
        group.add_argument('--command',
                           type=int,
                           required=False,
                           help='command ID')
        # Process options
        options = parser.parse_args()
        self.options = options
        # Check needed extra arguments
        if options.action == ACTION_STATUS:
            if not options.url:
                parser.error('missing URL argument')
        elif options.action == ACTION_GENERATE_KEYS:
            if not options.private_key:
                parser.error('missing private_key argument')
            if not options.public_key:
                parser.error('missing public_key argument')
        elif options.action == ACTION_HOST_REGISTER:
            if not options.token:
                parser.error('missing token argument')
        elif options.action == ACTION_HOST_VERIFY:
            if not options.token:
                parser.error('missing token argument')
        elif options.action == ACTION_COMMAND_GET:
            if not options.command:
                parser.error('missing command argument')

    def process(self):
        status = -1
        results = None
        api = Api(url=self.options.url)
        headers = {}
        # Save token authorization if passed in the arguments
        if self.options.token:
            headers['Authorization'] = f'Token {self.options.token}'
        if self.options.action == ACTION_STATUS:
            # Get status
            results = api.get(headers=headers)
            status = 0
            # Update settings
            self.settings.set_value(section=SECTION_SERVER,
                                    option=SERVER_URL,
                                    value=results[SERVER_URL])
            self.settings.set_value(section=SECTION_ENDPOINTS,
                                    option=ACTION_DISCOVER,
                                    value=results[ACTION_DISCOVER])
        elif self.options.action == ACTION_DISCOVER:
            # Discover services URLS
            api.url = self.build_url(section=SECTION_ENDPOINTS,
                                     option=ACTION_DISCOVER)
            results = api.get(headers=headers)
            status = 0
            # Update settings
            for endpoint in results[ENDPOINTS_FIELD]:
                self.settings.set_value(
                    section=SECTION_ENDPOINTS,
                    option=endpoint,
                    value=results[ENDPOINTS_FIELD][endpoint])
        elif self.options.action == ACTION_GENERATE_KEYS:
            # Generate private and public keys and save them in two files
            key = RsaKey()
            key.create_new_key(size=4096)
            key.save_private_key(filename=self.options.private_key)
            key.save_public_key(filename=self.options.public_key)
            status = 0
            # Update settings
            self.settings.set_value(section=SECTION_HOST,
                                    option=OPTION_PRIVATE_KEY,
                                    value=self.options.private_key)
            self.settings.set_value(section=SECTION_HOST,
                                    option=OPTION_PUBLIC_KEY,
                                    value=self.options.public_key)
        elif self.options.action == ACTION_HOST_REGISTER:
            if not self.load_uuid():
                # Host registration
                api.url = self.build_url(section=SECTION_ENDPOINTS,
                                         option=ACTION_HOST_REGISTER)
                data = {PUBLIC_KEY_FIELD: self.key.get_public_key_content()}
                results = api.post(headers=headers,
                                   data=data)
                status = 0
                # Update settings
                self.settings.set_value(section=SECTION_HOST,
                                        option=UUID_FIELD,
                                        value=results[ENCRYPTED_FIELD])
            else:
                # Host already registered
                results = {STATUS_FIELD: STATUS_ERROR,
                           MESSAGE_FIELD: 'Host UUID already set'}
                status = 1
        elif self.options.action == ACTION_HOST_VERIFY:
            # Load private key and encrypt UUID
            message_encrypted = self.key.sign(text=STATUS_OK,
                                              use_base64=True)
            # Host verification
            api.url = self.build_url(section=SECTION_ENDPOINTS,
                                     option=ACTION_HOST_VERIFY)
            data = {UUID_FIELD: self.load_uuid(),
                    ENCRYPTED_FIELD: message_encrypted}
            results = api.post(headers=headers,
                               data=data)
            status = 0
            # Save token
            self.settings.set_value(section=SECTION_HOST,
                                    option=OPTION_TOKEN,
                                    value=results[ENCRYPTED_FIELD])
        elif self.options.action == ACTION_COMMANDS_LIST:
            # List commands
            api.url = self.build_url(section=SECTION_ENDPOINTS,
                                     option=ACTION_COMMANDS_LIST)
            results = api.get(headers=headers)
            status = 0
        elif self.options.action == ACTION_COMMAND_GET:
            # Execute command
            api.url = self.build_url(section=SECTION_ENDPOINTS,
                                     option=ACTION_COMMAND_GET,
                                     extra=f'{self.options.command}/')
            results = api.get(headers=headers)
            # Check if there's a valid command in the command
            if 'id' in results and results['id'] == self.options.command:
                # Create a new temporary file with the decrypted command
                _, temp_file_source = tempfile.mkstemp(
                    prefix=f'{PRODUCT_NAME.lower().replace(" ", "_")}-',
                    text=True)
                with open(temp_file_source, 'w') as file:
                    file.write('__RESULT__ = ""'
                               '\n'
                               '\n')
                    file.write(self.key.decrypt(text=results['command'],
                                                use_base64=True))
                    # Write __RESULT__ variable in stderr
                    file.write('\n'
                               '\n'
                               'import sys\n'
                               'sys.stderr.write(__RESULT__)\n')
                # Execute the source code in a Python process
                process = subprocess.Popen(args=['python', temp_file_source],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                stdout, stderr = process.communicate(timeout=15)
                print(f'{stdout=}')
                print(f'{stderr=}')
                # Remove the temporary file
                try:
                    os.remove(path=temp_file_source)
                except FileNotFoundError:
                    # File was already removed
                    pass
                status = 0
            else:
                # Invalid command
                status = 1
        return status, results

    def load(self):
        """
        Load settings
        :return: None
        """
        self.settings = Settings()
        if self.options.settings:
            self.settings.load(self.options.settings)
        # Load private and public keys if available
        if priv_key_path := self.settings.get_value(section=SECTION_HOST,
                                                    option=OPTION_PRIVATE_KEY):
            self.key = RsaKey()
            self.key.load_private_key_from_file(filename=priv_key_path)
            self.key.load_public_key_from_private_key()

    def save(self):
        """
        Save settings
        :return: None
        """
        if self.options.settings:
            self.settings.save(self.options.settings)

    def build_url(self, section: str, option: str, extra: str = None) -> str:
        """
        Build URL from settings option
        :param section: settings section
        :param option: settings option
        :return: resulting URL
        """
        return self.settings.build_url(
                url=self.settings.get_value(section=section,
                                            option=option),
                extra=extra)

    def load_uuid(self) -> str:
        """
        Load UUID from settings
        :return: host UUID
        """
        if encrypted_data := self.settings.get_value(section=SECTION_HOST,
                                                     option=UUID_FIELD):
            results = self.key.decrypt(text=encrypted_data,
                                       use_base64=True)
        else:
            results = None
        return results


if __name__ == '__main__':
    client = Client()
    # Get command line arguments
    client.get_command_line()
    # Load settings
    client.load()
    # Process the arguments
    status, results = client.process()
    if results is not None:
        # Show the results
        print(results)
    # Save settings
    client.save()
    # Set exit code accordingly to the executed action
    sys.exit(status)
