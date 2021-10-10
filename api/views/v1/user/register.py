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

import uuid

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from remotes.constants import STATUS_FIELD, STATUS_OK, UUID_FIELD


class UserRegisterView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        # Create a new user
        new_uuid = uuid.uuid4()
        get_user_model().objects.create(username=new_uuid,
                                        is_active=False)
        return Response(data={STATUS_FIELD: STATUS_OK,
                              UUID_FIELD: new_uuid},
                        status=status.HTTP_200_OK)
