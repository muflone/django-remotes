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

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from project import PRODUCT_NAME, VERSION

from remotes.constants import (API_VERSION, SERVER_URL,
                               STATUS_FIELD, STATUS_OK)

from utility.misc.get_setting_value import get_setting_value


class StatusView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        server_url = get_setting_value(name=SERVER_URL)
        separator = '' if server_url.endswith('/') else '/'
        return Response(data={STATUS_FIELD: STATUS_OK,
                              'app_name': PRODUCT_NAME,
                              'version': VERSION,
                              SERVER_URL: server_url,
                              'api_url': f'{server_url}'
                                         f'{separator}'
                                         f'{API_VERSION}/'},
                        status=status.HTTP_200_OK)
