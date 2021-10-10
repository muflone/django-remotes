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

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class Keys(object):
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_new_rsa_key(self, size: int):
        """
        Generate new private and public keys
        :param size: key size in bytes
        :return: None
        """
        self.private_key = rsa.generate_private_key(public_exponent=65537,
                                                    key_size=size)
        self.public_key = self.private_key.public_key()

    def get_private_key_content(self, password: str = None) -> bytes:
        """
        Get the private key content
        :param password: passphrase used to encrypt the private key
        :return: private key content
        """
        encryption = (serialization.BestAvailableEncryption(password=password)
                      if password is not None
                      else serialization.NoEncryption())
        result = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption)
        return result

    def get_public_key_content(self) -> bytes:
        """
        Get the public key content
        :return: public key content
        """
        result = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return result

    def load_private_key(self, filename: str, password: str = None):
        """
        Load private key from filename using the provided optional password
        :param filename: source filename to load the priva key
        :return: None
        """
        with open(file=filename, mode='rb') as file:
            self.private_key = serialization.load_pem_private_key(
                data=file.read(),
                password=password)
        return self.private_key

    def load_public_key(self, filename: str):
        """
        Load public key from filename
        :param filename: source filename to load the public key
        :return: None
        """
        with open(file=filename, mode='rb') as file:
            self.public_key = serialization.load_pem_public_key(
                data=file.read())
        return self.public_key

    def save_private_key(self, filename: str, password: str = None):
        """
        Save the private key to file
        :param filename: destination filename to save the private key
        :param password: passphrase used to encrypt the private key
        :return: None
        """
        with open(file=filename, mode='wb') as file:
            file.write(self.get_private_key_content(password=password))

    def save_public_key(self, filename: str):
        """
        Save the public key to file
        :param filename: destination filename to save the public key
        :return: None
        """
        with open(file=filename, mode='wb') as file:
            file.write(self.get_public_key_content())
