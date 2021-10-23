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

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from api.permissions import IsUserWithHost
from api.views.retrieve_api_encrypted import RetrieveAPIEncryptedView

from remotes.models import CommandsGroupItem, Host


class CommandGetSerializer(ModelSerializer):
    """
    Serializer for CommandGetView
    """
    command = SerializerMethodField('get_command')

    class Meta:
        model = CommandsGroupItem
        fields = ['id', 'name', 'command']

    def get_command(self, instance):
        return instance.command.command


class CommandGetView(RetrieveAPIEncryptedView):
    model = CommandsGroupItem
    permission_classes = (IsUserWithHost, )
    serializer_class = CommandGetSerializer
    encrypted_fields = ['name', 'command']

    def get_queryset(self):
        # Find host matching with the user
        host = Host.objects.get(user=self.request.user)
        # Find the commands group item
        queryset = self.model.objects.filter(pk=self.kwargs['pk'],
                                             group__hosts__hosts=host.id)
        return queryset
