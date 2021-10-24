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
from rest_framework.serializers import CharField, IntegerField, Serializer

from rest_framework.views import APIView

from api.permissions import IsUserWithHost

from encryption.fernet_encrypt import FernetEncrypt

from remotes.constants import (ID_FIELD,
                               RESULTS_FIELD,
                               STATUS_FIELD,
                               STATUS_OK,
                               STATUS_ERROR)
from remotes.models import CommandsGroupItem, CommandsOutput, Host, Variable


class CommandPostSerializer(Serializer):
    """
    Serializer for CommandPostView
    """
    id = IntegerField(required=True)
    output = CharField(required=True,
                       allow_blank=True)
    result = CharField(required=True,
                       allow_blank=True)

    def create(self, data) -> CommandsOutput:
        """
        Create new CommandsOutput object
        :param data: data to save
        :return: new CommandsOutput object
        """
        results = CommandsOutput.objects.create(group_item_id=data['id'],
                                                output=data['output'],
                                                result=data['result'])
        return results


class CommandPostView(APIView):
    permission_classes = (IsUserWithHost, )

    def post(self, request, *args, **kwargs):
        """
        Create new object
        """
        # Find host matching with the user
        host = Host.objects.get(user=self.request.user)
        # Find the CommandGroupItem and check if it's in the same host group
        command_group_item = CommandsGroupItem.objects.filter(
            pk=kwargs['pk'],
            group__hosts__hosts=host.id).first()
        if command_group_item:
            serializer = CommandPostSerializer(data=request.data.copy())
            # Add ID to the data from the querystring
            serializer.initial_data['id'] = kwargs['pk']
            # Decrypt data using the host UUID
            decryptor = FernetEncrypt()
            decryptor.load_key_from_uuid(host.uuid)
            serializer.initial_data['output'] = decryptor.decrypt(
                text=request.data['output'])
            serializer.initial_data['result'] = decryptor.decrypt(
                text=request.data['result'])
            # Process the data
            if serializer.is_valid():
                # Save data creating a new CommandOutput object
                command_output = serializer.save()
                if command_output.group_item.variable:
                    # Save result in variable
                    variable, _ = Variable.objects.get_or_create(
                        host=host,
                        name=command_output.group_item.variable)
                    variable.raw_value = command_output.result
                    variable.save()
                # Show results
                results = {ID_FIELD: serializer.data['id']}
                return Response(data={STATUS_FIELD: STATUS_OK,
                                      RESULTS_FIELD: results},
                                status=status.HTTP_201_CREATED)
            else:
                # Show errors
                results = serializer.errors.copy()
                results[STATUS_FIELD] = STATUS_ERROR
                return Response(data=results,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            # Unauthorized host
            results = {STATUS_FIELD: STATUS_ERROR}
            return Response(data=results,
                            status=status.HTTP_403_FORBIDDEN)
