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

import urllib.parse

from django.urls import reverse

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from project import PRODUCT_NAME, VERSION

from remotes.client.actions import ACTION_DISCOVER
from remotes.constants import (API_VERSION, SERVER_URL,
                               STATUS_FIELD, STATUS_OK)

from utility.misc.get_setting_value import get_setting_value


class StatusView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        server_url = get_setting_value(name=SERVER_URL)
        # Auto-detect the server_url if it wasn't configured
        if not server_url:
            server_url = f'{request.scheme}://{request.get_host()}'
        return Response(
            data={STATUS_FIELD: STATUS_OK,
                  'app_name': PRODUCT_NAME,
                  'version': VERSION,
                  SERVER_URL: urllib.parse.urljoin(base=server_url,
                                                   url='/'),
                  ACTION_DISCOVER: reverse(f'api.{API_VERSION}.discover')},
            status=status.HTTP_200_OK)
