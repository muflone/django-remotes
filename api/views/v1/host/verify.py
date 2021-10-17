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

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from client.keys import Keys

from remotes.constants import (ENCRYPTED_FIELD,
                               MESSAGE_FIELD,
                               STATUS_FIELD,
                               STATUS_ERROR,
                               STATUS_OK,
                               UUID_FIELD)
from remotes.models import Host


class HostVerifyView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
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
            keys = Keys()
            keys.load_public_key(data=host.pubkey)
            if not keys.verify(data=message_encrypted,
                               text=STATUS_OK,
                               use_base64=True):
                return Response(data={STATUS_FIELD: STATUS_ERROR,
                                      MESSAGE_FIELD: 'Invalid signature'},
                                status=status.HTTP_400_BAD_REQUEST)
            # Update host with the new user
            new_user = get_user_model().objects.create(username=host_uuid,
                                                       is_active=True)
            host.user = new_user
            host.is_active = True
            host.save()
            # Create new token for the user
            new_token = Token.objects.create(user=new_user)
            return Response(data={STATUS_FIELD: STATUS_OK,
                                  ENCRYPTED_FIELD: keys.encrypt(
                                      text=new_token.key,
                                      use_base64=True)},
                            status=status.HTTP_200_OK)
        else:
            # Host not found
            return Response(data={STATUS_FIELD: STATUS_ERROR,
                                  MESSAGE_FIELD: 'Host not found'},
                            status=status.HTTP_400_BAD_REQUEST)
