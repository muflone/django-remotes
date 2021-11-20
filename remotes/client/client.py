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
import pathlib
import subprocess
import tempfile
import urllib.parse
import uuid

from encryption.fernet_encrypt import FernetEncrypt
from encryption.rsa_key import RsaKey

from project import PRODUCT_NAME, VERSION

import remotes
from remotes.client.actions import (ACTION_COMMAND_GET,
                                    ACTION_COMMAND_POST,
                                    ACTION_COMMANDS_LIST,
                                    ACTION_COMMANDS_MONITOR,
                                    ACTION_COMMANDS_PROCESS,
                                    ACTION_DISCOVER,
                                    ACTION_GENERATE_KEYS,
                                    ACTION_HOST_REGISTER,
                                    ACTION_HOST_STATUS,
                                    ACTION_HOST_VERIFY,
                                    ACTION_NEW_HOST,
                                    ACTION_STATUS,
                                    ACTIONS)
from remotes.client.api import Api
from remotes.client.recurring_job import RecurringJob
from remotes.client.settings import (Settings,
                                     OPTION_PRIVATE_KEY,
                                     OPTION_PUBLIC_KEY,
                                     OPTION_TOKEN,
                                     SECTION_ENDPOINTS,
                                     SECTION_HOST,
                                     SECTION_SERVER)
from remotes.constants import (COMMAND_FIELD,
                               COMMANDS_RESULTS_FIELD,
                               ENCRYPTED_FIELD,
                               ENCRYPTION_KEY_FIELD,
                               ENDPOINTS_FIELD,
                               MESSAGE_FIELD,
                               METHOD_GET,
                               METHOD_POST,
                               PUBLIC_KEY_FIELD,
                               RESULTS_FIELD,
                               SERVER_URL,
                               STATUS_FIELD,
                               STATUS_ERROR,
                               STATUS_OK,
                               UUID_FIELD)

from utility.misc.python_version_action import PythonVersionAction


class Client(object):
    def __init__(self):
        self.options = None
        self.settings = None
        self.key = None
        self.encryptor = None

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
        parser.add_argument('--python', '-P',
                            action=PythonVersionAction,
                            help='show Python version')
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
        group.add_argument('--interval',
                           type=int,
                           required=False,
                           help='interval in seconds for commands monitoring')
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
        elif options.action == ACTION_NEW_HOST:
            if not options.url:
                parser.error('missing URL argument')
            if not options.token:
                parser.error('missing token argument')
            if not options.private_key:
                parser.error('missing private_key argument')
            if not options.public_key:
                parser.error('missing public_key argument')
        elif options.action == ACTION_COMMAND_GET:
            if not options.command:
                parser.error('missing command argument')
        elif options.action == ACTION_COMMANDS_MONITOR:
            if not options.interval:
                parser.error('missing monitoring interval')

    def process(self) -> tuple[int, dict]:
        """
        Process the command line action
        :return: tuple containing status code and dictionary with results
        """
        # actions map with (method, {kwargs for method})
        if self.options.action == ACTION_STATUS:
            # Get status
            status, results = self.do_get_status(url=self.options.url)
        elif self.options.action == ACTION_DISCOVER:
            # Discover services URLS
            status, results = self.do_discover()
        elif self.options.action == ACTION_GENERATE_KEYS:
            # Generate private and public keys and save them in two files
            status, results = self.do_generate_keys(
                private_key_filename=self.options.private_key,
                public_key_filename=self.options.public_key)
        elif self.options.action == ACTION_HOST_REGISTER:
            # Host registration
            status, results = self.do_host_register(
                token=self.options.token)
        elif self.options.action == ACTION_HOST_VERIFY:
            # Host verification
            status, results = self.do_host_verify(
                token=self.options.token)
        elif self.options.action == ACTION_HOST_STATUS:
            # Host status
            status, results = self.do_host_status()
        elif self.options.action == ACTION_NEW_HOST:
            # Generate private and public keys and save them in two files
            self.do_generate_keys(
                private_key_filename=self.options.private_key,
                public_key_filename=self.options.public_key)
            # Get status
            self.do_get_status(url=self.options.url)
            # Discover services URLS
            self.do_discover()
            # Host registration
            status, results = self.do_host_register(token=self.options.token)
            if status == 0:
                # Host verification
                status, results = self.do_host_verify(
                    token=self.options.token)
        elif self.options.action == ACTION_COMMANDS_LIST:
            # List commands
            status, results = self.do_list_commands()
        elif self.options.action == ACTION_COMMAND_GET:
            # Execute command
            status, results = self.do_get_command(
                command_id=self.options.command)
        elif self.options.action == ACTION_COMMANDS_MONITOR:
            # Monitor for commands to execute
            status, results = self.do_monitor_commands(
                interval=self.options.interval)
        elif self.options.action == ACTION_COMMANDS_PROCESS:
            # Process every command
            status, results = self.do_process_commands()
        else:
            # Unexpected action
            status = -1
            results = None
        return status, results

    # noinspection PyMethodMayBeStatic
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
        status_url = urllib.parse.urljoin(base=url,
                                          url='api/status')
        results = self.do_api_request(method=METHOD_GET,
                                      url=status_url)
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
        self.key = key
        # Update settings
        self.settings.set_value(section=SECTION_HOST,
                                option=OPTION_PRIVATE_KEY,
                                value=os.path.abspath(private_key_filename))
        self.settings.set_value(section=SECTION_HOST,
                                option=OPTION_PUBLIC_KEY,
                                value=os.path.abspath(public_key_filename))
        return 0, None

    def do_host_register(self, token: str) -> tuple[int, dict]:
        """
        Discover services URLS

        :param token: authorization token
        :return: tuple with the status and the resulting data
        """
        try:
            uuid_field = self.decrypt_option(section=SECTION_HOST,
                                             option=UUID_FIELD)
        except ValueError:
            # UUID was encrypted with an invalid key
            uuid_field = None
        if not uuid_field:
            # Host registration
            url = self.build_url(section=SECTION_ENDPOINTS,
                                 option=ACTION_HOST_REGISTER)
            headers = {'Authorization': f'Token {token}'}
            data = {PUBLIC_KEY_FIELD: self.key.get_public_key_content()}
            results = self.do_api_request(method=METHOD_POST,
                                          url=url,
                                          headers=headers,
                                          data=data)
            # Check response status
            if STATUS_FIELD in results:
                status = 0
                # Update settings
                self.settings.set_value(section=SECTION_HOST,
                                        option=UUID_FIELD,
                                        value=results[ENCRYPTED_FIELD])
            else:
                # Unable to register host
                status = 2
        else:
            # Host already registered
            results = {STATUS_FIELD: STATUS_ERROR,
                       MESSAGE_FIELD: 'Host UUID already set'}
            status = 1
        return status, results

    def do_host_status(self) -> tuple[int, dict]:
        """
        Host status

        :return: tuple with the status and the resulting data
        """
        url = self.build_url(section=SECTION_ENDPOINTS,
                             option=ACTION_HOST_STATUS)
        token = self.decrypt_option(section=SECTION_HOST,
                                    option=OPTION_TOKEN)
        headers = {'Authorization': f'Token {token}'}
        results = self.do_api_request(method=METHOD_GET,
                                      url=url,
                                      headers=headers,
                                      data=None)
        return 0, results

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
            timeout = results['timeout']
            # Get the symmetric key used to decrypt the command to process
            decryptor = FernetEncrypt()
            decryptor.load_key(key=self.key.decrypt(
                text=results[ENCRYPTION_KEY_FIELD],
                use_base64=True))
            # Create a new temporary file with the decrypted command
            temp_file_fd, temp_file_source = tempfile.mkstemp(
                prefix=f'{PRODUCT_NAME.lower().replace(" ", "_")}-',
                text=True)
            with os.fdopen(temp_file_fd, 'w') as file:
                # Initialize modules path
                remotes_path = pathlib.Path(remotes.__path__[0])
                file.write('import sys\n'
                           f'sys.path.append(r"{remotes_path.parent}")\n')
                # Initialize __RESULT__ variable
                file.write('__RESULT__ = ""\n')
                # Save settings
                items = {key: decryptor.decrypt(text=value)
                         for key, value in results['settings'].items()}
                file.write(f'__SETTINGS__ = {items}\n')
                # Save variables
                items = {key: decryptor.decrypt(text=value) if value
                         else None
                         for key, value in results['variables'].items()}
                file.write(f'__VARIABLES__ = {items}\n')
                file.write('\n')
                # Write command
                file.write(decryptor.decrypt(text=results['command']))
                # Convert __RESULT__ in list if it's not a list and
                # write __RESULT__ in JSON format in stderr
                file.write('\n'
                           '\n'
                           'import json\n'
                           'import sys\n'
                           'if not isinstance(__RESULT__, list):\n'
                           '    __RESULT__ = [__RESULT__]\n'
                           'sys.stderr.write(json.dumps(obj=__RESULT__,\n'
                           '                            indent=2))\n')
            # Execute the source code in a Python process
            process = subprocess.Popen(args=['python', temp_file_source],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            try:
                stdout, stderr = [stream.decode('utf-8')
                                  for stream
                                  in process.communicate(timeout=timeout)]
                status = process.returncode
            except subprocess.TimeoutExpired:
                status = -1
                stdout = None
                stderr = None
                results['output'] = {STATUS_FIELD: STATUS_ERROR,
                                     MESSAGE_FIELD: 'timeout'}
            # Remove the temporary file
            try:
                os.remove(path=temp_file_source)
            except FileNotFoundError:
                # File was already removed
                pass
            # Transmit command results
            if stdout is not None:
                url = self.build_url(section=SECTION_ENDPOINTS,
                                     option=ACTION_COMMAND_POST,
                                     extra=f'{command_id}/')
                data = {'output': self.encryptor.encrypt(text=stdout),
                        'result': self.encryptor.encrypt(text=stderr)}
                post_results = self.do_api_request(method=METHOD_POST,
                                                   url=url,
                                                   headers=headers,
                                                   data=data)
                # Save results
                results['stdout'] = stdout
                results['stderr'] = stderr
                results['output'] = post_results
        else:
            # Invalid command
            status = 1
        return status, results

    def do_process_commands(self) -> tuple[int, dict]:
        """
        Execute every command in list

        :return: tuple with the status and the resulting data
        """
        status, results = self.do_list_commands()
        commands_results = {}
        results[COMMANDS_RESULTS_FIELD] = commands_results
        for command in results[RESULTS_FIELD]:
            # Process each command
            command_id = command[COMMAND_FIELD]
            _, commands_results[command_id] = self.do_get_command(
                command_id=command_id)
        return status, results

    def do_monitor_commands(self, interval: int) -> tuple[int, None]:
        """
        Monitor pending commands

        :param interval: interval in seconds to watch for commands to process
        :return: None
        """
        def monitor_process_commands() -> bool:
            """
            Process commands and always return True in order to continue with
            monitoring for new commands

            :return: True
            """
            self.do_process_commands()
            return True

        recurring = RecurringJob()
        recurring.add_job(delay=interval,
                          action=monitor_process_commands)
        recurring.run()
        return 0, None

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
            try:
                self.key = RsaKey()
                self.key.load_private_key_from_file(filename=priv_key_path)
                self.key.load_public_key_from_private_key()
            except FileNotFoundError:
                self.key = None
        if self.key and self.settings.get_value(section=SECTION_HOST,
                                                option=UUID_FIELD):
            # Initialize encryptor
            try:
                self.encryptor = FernetEncrypt()
                self.encryptor.load_key_from_uuid(guid=uuid.UUID(
                    hex=self.decrypt_option(section=SECTION_HOST,
                                            option=UUID_FIELD)))
            except ValueError:
                self.encryptor = None

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
            try:
                results = self.key.decrypt(text=encrypted_data,
                                           use_base64=True)
            except ValueError:
                # Invalid encrypted data
                results = None
        else:
            results = None
        return results
