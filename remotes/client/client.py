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
                               METHOD_GET,
                               METHOD_POST,
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

    def get_command_line(self) -> None:
        """
        Parse command line arguments
        :return: None
        """
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

    def process(self) -> tuple[int, dict]:
        """
        Process the command line action
        :return: tuple containing status code and dictionary with results
        """
        # actions map with (method, {kwargs for method})
        actions = {
            # Get status
            ACTION_STATUS: (self.do_get_status,
                            {'url': self.options.url}),
            # Discover services URLS
            ACTION_DISCOVER: (self.do_discover,
                              {}),
            # Generate private and public keys and save them in two files
            ACTION_GENERATE_KEYS: (self.do_generate_keys,
                                   {'private_key_filename':
                                    self.options.private_key,
                                    'public_key_filename':
                                    self.options.public_key}),
            # Host registration
            ACTION_HOST_REGISTER: (self.do_host_register,
                                   {'token': self.options.token}),
            # Host verification
            ACTION_HOST_VERIFY: (self.do_host_verify,
                                 {'token': self.options.token}),
            # List commands
            ACTION_COMMANDS_LIST: (self.do_list_commands,
                                   {}),
            # Execute command
            ACTION_COMMAND_GET: (self.do_get_command,
                                 {'command_id': self.options.command})
           }
        if self.options.action in actions:
            # Process action and get status and results
            method, kwargs = actions[self.options.action]
            status, results = method(**kwargs)
        else:
            # Unexpected action
            status = -1
            results = None
        return status, results

    def do_api_request(self,
                       method: str,
                       url: str,
                       headers: dict = None,
                       data: dict = None) -> dict:
        """
        Execute an API request for the selected URL
        :param method: REST method to execute
        :param url: URL to process
        :param headers: dictionary with headers to pass
        :param data: dictionary with data to pass
        :return: resulting data response
        """
        if headers is None:
            headers = {}
        api = Api(url=url)
        if method == METHOD_GET:
            results = api.get(headers=headers)
        elif method == METHOD_POST:
            results = api.post(headers=headers,
                               data=data)
        else:
            results = None
        return results

    def do_get_status(self, url: str) -> tuple[int, dict]:
        """
        Get status
        :param url: URL to request
        :return: tuple with the status and the resulting data
        """
        results = self.do_api_request(method=METHOD_GET,
                                      url=url)
        # Update settings
        self.settings.set_value(section=SECTION_SERVER,
                                option=SERVER_URL,
                                value=results[SERVER_URL])
        self.settings.set_value(section=SECTION_ENDPOINTS,
                                option=ACTION_DISCOVER,
                                value=results[ACTION_DISCOVER])
        return 0, results

    def do_discover(self) -> tuple[int, dict]:
        """
        Discover services URLS
        :return: tuple with the status and the resulting data
        """
        url = self.build_url(section=SECTION_ENDPOINTS,
                             option=ACTION_DISCOVER)
        results = self.do_api_request(method=METHOD_GET,
                                      url=url,
                                      data=None)
        # Update settings
        for endpoint in results[ENDPOINTS_FIELD]:
            self.settings.set_value(
                section=SECTION_ENDPOINTS,
                option=endpoint,
                value=results[ENDPOINTS_FIELD][endpoint])
        return 0, results

    def do_generate_keys(self,
                         private_key_filename: str,
                         public_key_filename: str) -> tuple[int, None]:
        """
        Generate private and public keys and save them in two files
        :param private_key_filename: filename where to save the private key
        :param public_key_filename: filename where to save the public key
        :return: tuple with the status and the resulting data
        """
        key = RsaKey()
        key.create_new_key(size=4096)
        key.save_private_key(filename=private_key_filename)
        key.save_public_key(filename=public_key_filename)
        # Update settings
        self.settings.set_value(section=SECTION_HOST,
                                option=OPTION_PRIVATE_KEY,
                                value=private_key_filename)
        self.settings.set_value(section=SECTION_HOST,
                                option=OPTION_PUBLIC_KEY,
                                value=public_key_filename)
        return 0, None

    def do_host_register(self, token: str) -> tuple[int, dict]:
        """
        Discover services URLS
        :param token: authorization token
        :return: tuple with the status and the resulting data
        """
        if not self.decrypt_option(section=SECTION_HOST, option=UUID_FIELD):
            # Host registration
            url = self.build_url(section=SECTION_ENDPOINTS,
                                 option=ACTION_HOST_REGISTER)
            headers = {'Authorization': f'Token {token}'}
            data = {PUBLIC_KEY_FIELD: self.key.get_public_key_content()}
            results = self.do_api_request(method=METHOD_POST,
                                          url=url,
                                          headers=headers,
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
        return status, results

    def do_host_verify(self, token: str) -> tuple[int, dict]:
        """
        Host verification
        :param token: authorization token
        :return: tuple with the status and the resulting data
        """
        message_encrypted = self.key.sign(text=STATUS_OK,
                                          use_base64=True)
        url = self.build_url(section=SECTION_ENDPOINTS,
                             option=ACTION_HOST_VERIFY)
        headers = {'Authorization': f'Token {token}'}
        data = {UUID_FIELD: self.decrypt_option(section=SECTION_HOST,
                                                option=UUID_FIELD),
                ENCRYPTED_FIELD: message_encrypted}
        results = self.do_api_request(method=METHOD_POST,
                                      url=url,
                                      headers=headers,
                                      data=data)
        # Save token
        self.settings.set_value(section=SECTION_HOST,
                                option=OPTION_TOKEN,
                                value=results[ENCRYPTED_FIELD])
        return 0, results

    def do_list_commands(self) -> tuple[int, dict]:
        """
        List commands
        :return: tuple with the status and the resulting data
        """
        url = self.build_url(section=SECTION_ENDPOINTS,
                             option=ACTION_COMMANDS_LIST)
        token = self.decrypt_option(section=SECTION_HOST,
                                    option=OPTION_TOKEN)
        headers = {'Authorization': f'Token {token}'}
        results = self.do_api_request(method=METHOD_GET,
                                      url=url,
                                      headers=headers,
                                      data=None)
        return 0, results

    def do_get_command(self, command_id: int) -> tuple[int, dict]:
        """
        Execute command
        :param command_id: command ID to execute
        :return: tuple with the status and the resulting data
        """
        url = self.build_url(section=SECTION_ENDPOINTS,
                             option=ACTION_COMMAND_GET,
                             extra=f'{command_id}/')
        token = self.decrypt_option(section=SECTION_HOST,
                                    option=OPTION_TOKEN)
        headers = {'Authorization': f'Token {token}'}
        results = self.do_api_request(method=METHOD_GET,
                                      url=url,
                                      headers=headers,
                                      data=None)
        # Check if there's a valid command in the command
        if 'id' in results and results['id'] == command_id:
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

    def load(self) -> None:
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

    def save(self) -> None:
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
        :param extra: extra arguments for URL
        :return: resulting URL
        """
        return self.settings.build_url(
                url=self.settings.get_value(section=section,
                                            option=option),
                extra=extra)

    def decrypt_option(self, section: str, option: str) -> str:
        """
        Load UUID from settings
        :param section: setting section
        :param option: setting option
        :return: host UUID
        """
        if encrypted_data := self.settings.get_value(section=section,
                                                     option=option):
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
    process_status, process_results = client.process()
    if process_results is not None:
        # Show the results
        print(process_results)
    # Save settings
    client.save()
    # Set exit code accordingly to the executed action
    sys.exit(process_status)
