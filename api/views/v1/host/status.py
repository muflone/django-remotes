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
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsUserWithHost

from remotes.constants import (HOSTS_GROUPS,
                               ID_FIELD,
                               STATUS_FIELD,
                               STATUS_OK,
                               USER_ID_FIELD,
                               USER_NAME_FIELD)
from remotes.models import Host


class HostStatusView(APIView):
    permission_classes = (IsUserWithHost, )

    def get(self, request):
        """
        Show host status information
        """
        # Find host matching with the user
        host = Host.objects.get(user_id=self.request.user.pk)
        hosts_groups = host.hostsgroup_set.all()
        return Response(
            data={STATUS_FIELD: STATUS_OK,
                  ID_FIELD: host.pk,
                  USER_ID_FIELD: host.user.pk,
                  USER_NAME_FIELD: host.user.username,
                  HOSTS_GROUPS: hosts_groups.values('id', 'name')},
            status=status.HTTP_200_OK)
