##
#     Project: Django Remotes
# Description: A Django application to execute remote commands
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021-2022 Fabio Castelli
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

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import CanUserRegisterHosts
from api.views.save_request_mixin import SaveRequestMixin

from encryption.rsa_key import RsaKey

from remotes.constants import (ENCRYPTED_FIELD,
                               HOSTS_GROUP_AUTO_ADD,
                               MESSAGE_FIELD,
                               STATUS_FIELD,
                               STATUS_ERROR,
                               STATUS_OK,
                               UUID_FIELD)
from remotes.models import Host, HostsGroup

from utility.misc.get_setting_value import get_setting_value


class HostVerifyView(APIView, SaveRequestMixin):
    permission_classes = (CanUserRegisterHosts, )

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        # Save request
        self.save_request(request, args, kwargs)
        # Get host UUID
        try:
            host_uuid = request.data[UUID_FIELD]
        except KeyError:
            return Response(data={STATUS_FIELD: STATUS_ERROR,
                                  MESSAGE_FIELD: 'Missing host UUID'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Get encrypted text
        try:
            message_encrypted = request.data[ENCRYPTED_FIELD]
        except KeyError:
            return Response(data={STATUS_FIELD: STATUS_ERROR,
                                  MESSAGE_FIELD: 'Missing encrypted text'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Check user
        if get_user_model().objects.filter(username=host_uuid).first():
            return Response(data={STATUS_FIELD: STATUS_ERROR,
                                  MESSAGE_FIELD: 'User already existing'},
                            status=status.HTTP_400_BAD_REQUEST)
        if host := Host.objects.filter(uuid=host_uuid).first():
            # Check status
            key = RsaKey()
            key.load_public_key(data=host.pubkey)
            if not key.verify(data=message_encrypted,
                              text=STATUS_OK,
                              use_base64=True):
                return Response(data={STATUS_FIELD: STATUS_ERROR,
                                      MESSAGE_FIELD: 'Invalid signature'},
                                status=status.HTTP_400_BAD_REQUEST)
            # Create and update the user
            new_user = get_user_model().objects.create(username=host_uuid)
            new_user.username = str(new_user.pk).zfill(6)
            new_user.is_active = True
            new_user.save()
            # Update host with the new user
            host.user = new_user
            host.is_active = True
            host.save()
            # Create new token for the user
            new_token = Token.objects.create(user=new_user)
            # Automatically add host to the hosts group
            if group_auto_add := get_setting_value(name=HOSTS_GROUP_AUTO_ADD):
                if hosts_group := HostsGroup.objects.filter(
                        name=group_auto_add).first():
                    hosts_group.hosts.add(host)
            return Response(data={STATUS_FIELD: STATUS_OK,
                                  ENCRYPTED_FIELD: key.encrypt(
                                      text=new_token.key,
                                      use_base64=True)},
                            status=status.HTTP_200_OK)
        else:
            # Host not found
            return Response(data={STATUS_FIELD: STATUS_ERROR,
                                  MESSAGE_FIELD: 'Host not found'},
                            status=status.HTTP_400_BAD_REQUEST)
