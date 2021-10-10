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


def generate_keys(private_key_filename: str,
                  public_key_filename: str) -> None:
    """
    Generate private and public keys and save them
    :param private_key_filename: private key filename
    :param public_key_filename: public key filename
    """
    private_key = rsa.generate_private_key(public_exponent=65537,
                                           key_size=4096)
    # Save private key
    with open(file=private_key_filename, mode='wb') as file:
        file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()))
    # Save public key
    with open(file=public_key_filename, mode='wb') as file:
        file.write(private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo))


def load_private_key(filename: str, password: str = None):
    """
    Load private key from filename using the provided optional password
    """
    with open(file=filename, mode='rb') as file:
        result = serialization.load_pem_private_key(data=file.read(),
                                                    password=password)
    return result
