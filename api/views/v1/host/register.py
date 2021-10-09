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

from cryptography.hazmat.primitives import serialization

from remotes.constants import (MESSAGE_FIELD,
                               STATUS_FIELD, STATUS_ERROR, STATUS_OK)
from remotes.models import Host


class HostRegisterView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        host_uuid = request.data['uuid']
        host_key = request.data['key']
        # Check if the host with the same UUID already exists
        if not Host.objects.filter(uuid=host_uuid).first():
            # Inexistent host
            try:
                serialization.load_pem_public_key(
                    data=host_key.encode('utf-8'))
                # Create a new user and token
                new_user = get_user_model().objects.create(username=host_uuid,
                                                           is_active=False)
                Token.objects.create(user=new_user)
                # Register a new host
                Host.objects.create(name=host_uuid,
                                    uuid=host_uuid,
                                    pubkey=host_key)
                return Response(data={STATUS_FIELD: STATUS_OK},
                                status=status.HTTP_200_OK)
            except ValueError:
                # Invalid PEM key
                return Response(data={STATUS_FIELD: STATUS_ERROR,
                                      MESSAGE_FIELD: 'Invalid PEM key'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            # Existing host
            return Response(data={STATUS_FIELD: STATUS_ERROR,
                                  MESSAGE_FIELD: 'Existing host'},
                            status=status.HTTP_400_BAD_REQUEST)
