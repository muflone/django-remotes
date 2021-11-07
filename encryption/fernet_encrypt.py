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

import base64
from uuid import UUID

from cryptography.fernet import Fernet


class FernetEncrypt(object):
    def __init__(self):
        self._key = None

    def create_new_key(self):
        """
        Generate new encryption key
        :return: None
        """
        self._key = Fernet.generate_key()

    def get_key(self) -> bytes:
        """
        Return the encryption key
        :return: encryption key content
        """
        return self._key

    def load_key(self, key: bytes) -> None:
        """
        Load the encryption key
        :return: None
        """
        self._key = key

    def load_key_from_file(self, filename: str):
        """
        Load key from file
        :param filename: source filename from where to load the key
        :return: None
        """
        with open(file=filename, mode='rb') as file:
            self.load_key(key=file.read())

    def load_key_from_uuid(self, guid: UUID):
        """
        Load key from UUID
        :param guid: UUID object
        :return: None
        """
        self.load_key(key=base64.b64encode(guid.hex.encode('utf-8')))

    def save_key_to_file(self, filename: str):
        """
        Save the key to file
        :param filename: destination filename where to save the key
        :return: None
        """
        with open(file=filename, mode='wb') as file:
            file.write(self._key)

    def encrypt(self, text: str) -> str:
        """
        Encrypt the input text using the key
        :param text: text to be encrypted
        :return: resulting encrypted text
        """
        return Fernet(self._key).encrypt(
            data=text.encode('utf-8')).decode('utf-8')

    def decrypt(self, text: str) -> str:
        """
        Decrypt the input text using the key
        :param text: encrypted text to decrypt
        :return: resulting plain text
        """
        return Fernet(self._key).decrypt(
            token=text.encode('utf-8')).decode('utf-8')
