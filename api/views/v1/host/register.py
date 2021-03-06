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

import uuid

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import CanUserRegisterHosts
from api.views.save_request_mixin import SaveRequestMixin

from encryption.rsa_key import RsaKey

from remotes.constants import (ENCRYPTED_FIELD,
                               MESSAGE_FIELD,
                               PUBLIC_KEY_FIELD,
                               STATUS_FIELD,
                               STATUS_ERROR,
                               STATUS_OK)
from remotes.models import Host


class HostRegisterView(APIView, SaveRequestMixin):
    permission_classes = (CanUserRegisterHosts,)

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        # Save request
        self.save_request(request, args, kwargs)
        # Get host public key
        try:
            host_key = request.data[PUBLIC_KEY_FIELD]
        except KeyError:
            return Response(data={STATUS_FIELD: STATUS_ERROR,
                                  MESSAGE_FIELD: 'Missing host public key'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Check public key
        try:
            key = RsaKey()
            key.load_public_key(data=host_key)
        except ValueError:
            # Invalid PEM key
            return Response(data={STATUS_FIELD: STATUS_ERROR,
                                  MESSAGE_FIELD: 'Invalid PEM key'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Create a new Host
        new_uuid = uuid.uuid4()
        # Register a new host
        Host.objects.create(uuid=new_uuid,
                            pubkey=key.get_public_key_content(),
                            user=None,
                            is_active=False)
        return Response(data={STATUS_FIELD: STATUS_OK,
                              ENCRYPTED_FIELD: key.encrypt(text=str(new_uuid),
                                                           use_base64=True)},
                        status=status.HTTP_200_OK)
