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

from remotes.models import CommandsGroupItem, Host, VariableValue


class CommandGetSerializer(ModelSerializer):
    """
    Serializer for CommandGetView
    """
    settings = SerializerMethodField('get_settings')
    variables = SerializerMethodField('get_variables')
    command = SerializerMethodField('get_command')
    command_name = SerializerMethodField('get_command_name')

    class Meta:
        model = CommandsGroupItem
        fields = ['id', 'settings', 'variables', 'command', 'command_name',
                  'timeout']

    # noinspection PyMethodMayBeStatic
    def get_settings(self, instance):
        return {item.name: item.value
                for item in instance.command.settings.all()}

    def get_variables(self, instance):
        # Initialize variable values to None
        variables = instance.command.variables.all()
        result = {item.name: None
                  for item in variables}
        # Find host matching with the user
        host = Host.objects.get(user=self.context['request'].user)
        # Update variable values
        variables_values = VariableValue.objects.filter(host=host,
                                                        variable__in=variables)
        for item in variables_values:
            result[item.variable.name] = item.value
        return result

    # noinspection PyMethodMayBeStatic
    def get_command(self, instance):
        return instance.command.command

    # noinspection PyMethodMayBeStatic
    def get_command_name(self, instance):
        return instance.command.name


class CommandGetView(RetrieveAPIEncryptedView):
    model = CommandsGroupItem
    permission_classes = (IsUserWithHost, )
    serializer_class = CommandGetSerializer
    encrypted_fields = ['name', 'settings', 'variables', 'command']

    def get_queryset(self):
        # Find host matching with the user
        host = Host.objects.get(user=self.request.user)
        # Find the commands group item
        queryset = self.model.objects_enabled.filter(
            pk=self.kwargs['pk'],
            group__is_active=True,
            group__hosts__hosts=host.pk,
            group__hosts__is_active=True)
        return queryset
