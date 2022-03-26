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

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import pgettext_lazy

from encryption.fernet_encrypt import FernetEncrypt
from encryption.rsa_key import RsaKey

from remotes.constants import ENCRYPTED_FIELD, ENCRYPTION_KEY_FIELD

from utility.actions import ActionSetActive, ActionSetInactive
from utility.models import (BaseModel, BaseModelAdmin,
                            ManagerEnabled, ManagerDisabled)


class Host(BaseModel):
    """
    Host
    """
    uuid = models.UUIDField(unique=True,
                            verbose_name=pgettext_lazy(
                                'Host',
                                'UUID'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy(
                                       'Host',
                                       'description'))
    pubkey = models.TextField(null=True,
                              blank=True,
                              verbose_name=pgettext_lazy(
                                  'Host',
                                  'public key'))
    user = models.OneToOneField(to=get_user_model(),
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                default=None,
                                verbose_name=pgettext_lazy(
                                    'Host',
                                    'user'))
    is_active = models.BooleanField(default=True,
                                    verbose_name=pgettext_lazy(
                                        'Host',
                                        'active'))

    # Set the managers for the model
    objects = models.Manager()
    objects_enabled = ManagerEnabled()
    objects_disabled = ManagerDisabled()

    class Meta:
        # Define the database table
        ordering = ['-is_active', 'user', 'uuid']
        verbose_name = pgettext_lazy('Host',
                                     'Host')
        verbose_name_plural = pgettext_lazy('Host',
                                            'Hosts')

    def __str__(self):
        # noinspection PyUnresolvedReferences
        return self.user.username if self.user else str(self.uuid)

    def encrypt_data(self, data: dict, fields: list) -> None:
        """
        Encrypt some fields in the `data` dictionary using a new symmetric key
        The new key will be saved in a field called `ENCRYPTION_KEY_FIELD`

        :param data: initial data to encrypt
        :param fields: fields list to encrypt
        :return: None
        """
        # Create a new symmetric key to encrypt the data
        encryptor = FernetEncrypt()
        encryptor.create_new_key()
        # Encrypt any field listed in encrypted_fields
        if fields:
            data[ENCRYPTED_FIELD] = []
        for field in fields:
            if field in data:
                if isinstance(data[field], list):
                    # Encrypt each value in list
                    for index, value in enumerate(data[field]):
                        if data[field][index] is not None:
                            data[field][index] = encryptor.encrypt(text=value)
                elif isinstance(data[field], dict):
                    # Encrypt each value in dict
                    for key, value in data[field].items():
                        if data[field][key] is not None:
                            data[field][key] = encryptor.encrypt(text=value)
                elif data[field] is not None:
                    # Encrypt other types field
                    data[field] = encryptor.encrypt(text=str(data[field]))
                data[ENCRYPTED_FIELD].append(field)
        # Encrypt the symmetric key using the asymmetric key
        if data[ENCRYPTED_FIELD]:
            # Obtain the host public key to encrypt the symmetric key
            key = RsaKey()
            key.load_public_key(data=self.pubkey)
            data[ENCRYPTION_KEY_FIELD] = key.encrypt(
                text=encryptor.get_key().decode('utf-8'),
                use_base64=True)


class HostAdmin(BaseModelAdmin,
                ActionSetActive,
                ActionSetInactive):
    actions = ['set_active', 'set_inactive']
    list_display = ('__str__', 'uuid', 'user', 'user_first_name',
                    'user_last_name', 'groups_list', 'description',
                    'is_active')
    list_filter = ('is_active',)
    ordering = ['user__username']
    readonly_fields = ('user_first_name', 'user_last_name', 'uuid',
                       'groups_list')

    # noinspection PyMethodMayBeStatic
    def groups_list(self, instance) -> str:
        """
        Return the HostsGroup names for the current host

        :param instance: Host instance
        :return: a comma separated list of groups
        """
        return ', '.join(instance.hostsgroup_set.values_list('name',
                                                             flat=True))

    # noinspection PyMethodMayBeStatic
    def user_first_name(self, instance) -> str:
        """
        Return the User first name for the current host

        :param instance: Host instance
        :return: user first name
        """
        return instance.user.first_name

    # noinspection PyMethodMayBeStatic
    def user_last_name(self, instance) -> str:
        """
        Return the User last name for the current host

        :param instance: Host instance
        :return: user last name
        """
        return instance.user.last_name
