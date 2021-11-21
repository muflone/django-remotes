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

from django.urls import reverse

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.views.save_request_mixin import SaveRequestMixin

from remotes.client.actions import (ACTION_COMMAND_GET,
                                    ACTION_COMMAND_POST,
                                    ACTION_COMMANDS_LIST,
                                    ACTION_HOST_REGISTER,
                                    ACTION_HOST_STATUS,
                                    ACTION_HOST_VERIFY)
from remotes.constants import ENDPOINTS_FIELD, STATUS_FIELD, STATUS_OK


class DiscoverView(APIView, SaveRequestMixin):
    permission_classes = (AllowAny, )

    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        # Save request
        self.save_request(request, args, kwargs)
        endpoints = {
            ACTION_COMMAND_GET: reverse('api.v1.command.get.generic'),
            ACTION_COMMAND_POST: reverse('api.v1.command.post.generic'),
            ACTION_COMMANDS_LIST: reverse('api.v1.commands.list'),
            ACTION_HOST_REGISTER: reverse('api.v1.host.register'),
            ACTION_HOST_STATUS: reverse('api.v1.host.status'),
            ACTION_HOST_VERIFY: reverse('api.v1.host.verify')
        }
        return Response(
            data={STATUS_FIELD: STATUS_OK,
                  ENDPOINTS_FIELD: endpoints},
            status=status.HTTP_200_OK)
