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

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


class RsaKey(object):
    def __init__(self):
        self._private_key = None
        self._public_key = None

    def create_new_key(self, size: int):
        """
        Generate new private and public keys

        :param size: key size in bytes
        :return: None
        """
        self._private_key = rsa.generate_private_key(public_exponent=65537,
                                                     key_size=size)
        self.load_public_key_from_private_key()

    def load_public_key_from_private_key(self) -> None:
        self._public_key = self._private_key.public_key()

    def get_private_key_bytes(self, password: str = None) -> bytes:
        """
        Get the private key content in bytes

        :param password: passphrase used to encrypt the private key
        :return: private key content
        """
        encryption = (
            serialization.BestAvailableEncryption(
                password=password.encode('utf-8'))
            if password is not None
            else serialization.NoEncryption())
        results = self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption)
        return results

    def get_private_key_content(self, password: str = None) -> str:
        """
        Get the private key content

        :param password: passphrase used to encrypt the private key
        :return: private key content
        """
        return self.get_private_key_bytes(password=password).decode('utf-8')

    def get_public_key_bytes(self) -> bytes:
        """
        Get the public key content in bytes

        :return: public key content
        """
        results = self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return results

    def get_public_key_content(self) -> str:
        """
        Get the public key content

        :return: public key content
        """
        return self.get_public_key_bytes().decode('utf-8')

    def load_private_key(self, data: str, password: str = None):
        """
        Load private key from string using the provided optional password

        :param data: private key content
        :param password: passphrase used to encrypt the private key
        :return: private key
        """
        self._private_key = serialization.load_pem_private_key(
            data=data.encode('utf-8'),
            password=password)
        return self._private_key

    def load_private_key_from_file(self, filename: str, password: str = None):
        """
        Load private key from filename using the provided optional password

        :param filename: source filename to load the private key
        :param password: passphrase used to encrypt the private key
        :return: private key
        """
        with open(file=filename, mode='r') as file:
            self._private_key = self.load_private_key(data=file.read(),
                                                      password=password)
        return self._private_key

    def load_public_key(self, data: str):
        """
        Load public key from a string

        :param data: public key content
        :return: public key
        """
        self._public_key = serialization.load_pem_public_key(
            data=data.encode('utf-8'))
        return self._public_key

    def load_public_key_from_file(self, filename: str):
        """
        Load public key from filename

        :param filename: source filename to load the public key
        :return: public key
        """
        with open(file=filename, mode='r') as file:
            self._public_key = self.load_public_key(data=file.read())
        return self._public_key

    def save_private_key(self, filename: str, password: str = None):
        """
        Save the private key to file

        :param filename: destination filename to save the private key
        :param password: passphrase used to encrypt the private key
        :return: None
        """
        with open(file=filename, mode='wb') as file:
            file.write(self.get_private_key_bytes(password=password))

    def save_public_key(self, filename: str):
        """
        Save the public key to file

        :param filename: destination filename to save the public key
        :return: None
        """
        with open(file=filename, mode='wb') as file:
            file.write(self.get_public_key_bytes())

    def encrypt(self, text: str, use_base64: bool) -> str:
        """
        Encrypt text using the public key

        :param text: text to be encrypted
        :param use_base64: encode encrypted text in base64
        :return: resulting encrypted text
        """
        encrypted = self._public_key.encrypt(
            plaintext=text.encode('utf-8'),
            padding=padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                 algorithm=hashes.SHA256(),
                                 label=None))
        results = encrypted if not use_base64 else base64.b64encode(encrypted)
        return results.decode('utf-8')

    def decrypt(self, text: str, use_base64: bool) -> str:
        """
        Decrypt text using the private key

        :param text: encrypted text to decrypt
        :param use_base64: encrypted text is in base64
        :return: resulting plain text
        """
        results = self._private_key.decrypt(
            ciphertext=text if not use_base64 else base64.b64decode(text),
            padding=padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                 algorithm=hashes.SHA256(),
                                 label=None))
        return results.decode('utf-8')

    def sign(self, text: str, use_base64: bool) -> str:
        """
        Sign text using the private key

        :param text: text to be signed
        :param use_base64: encrypted text is in base64
        :return: signed text
        """
        encrypted = self._private_key.sign(
            data=text.encode('utf-8'),
            padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                salt_length=padding.PSS.MAX_LENGTH),
            algorithm=hashes.SHA256())
        results = encrypted if not use_base64 else base64.b64encode(encrypted)
        return results.decode('utf-8')

    def verify(self, data: str, text: str, use_base64: bool) -> bool:
        """
        Verify encrypted text using the public key

        :param data: signature text to verify
        :param text: clear text to verify
        :param use_base64: encrypted text is in base64
        :return: resulting encrypted text
        """
        try:
            self._public_key.verify(
                signature=(data.encode('utf-8')
                           if not use_base64
                           else base64.b64decode(data)),
                data=text.encode('utf-8'),
                padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                    salt_length=padding.PSS.MAX_LENGTH),
                algorithm=hashes.SHA256())
            results = True
        except InvalidSignature:
            results = False
        return results

    def get_public_key_length(self) -> int:
        """
        Return the public key length in bits

        :return: key length in bit
        """
        return self._public_key.key_size
