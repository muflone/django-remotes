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

from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from api.permissions import IsUserWithHost

from remotes.constants import (COMMAND_FIELD,
                               GROUP_FIELD,
                               ID_FIELD,
                               RESULTS_FIELD,
                               STATUS_FIELD,
                               STATUS_OK)
from remotes.models import CommandsGroup, CommandsOutput, Host


class CommandsListView(ListAPIView):
    permission_classes = (IsUserWithHost, )

    def get(self, request, *args, **kwargs):
        results = []
        now = timezone.now()
        # Get all the already executed commands to exclude
        excluded = CommandsOutput.objects.filter(host__user_id=request.user.pk)
        # Get all the hosts group for the current user host
        hosts_group = Host.objects_enabled.filter(
            user_id=request.user.pk).first().hostsgroup_set.filter(
            is_active=True)
        # Get all the commands group for the hosts groups
        groups = CommandsGroup.objects_enabled.filter(hosts__in=hosts_group,
                                                      after__lt=now,
                                                      before__gt=now)
        for group in groups.order_by('order'):
            # Check each group and exclude items already processed
            items = group.command_set.exclude(
                id__in=excluded.values_list('command')).exclude(
                is_active=False)
            for command in items.order_by('order'):
                # Get each command in the group
                results.append({ID_FIELD: command.pk,
                                GROUP_FIELD: group.pk,
                                COMMAND_FIELD: command.pk})
        return Response(
            data={STATUS_FIELD: STATUS_OK,
                  RESULTS_FIELD: results},
            status=status.HTTP_200_OK)
