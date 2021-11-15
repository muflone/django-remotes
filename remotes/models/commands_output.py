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

from django.db import models
from django.utils.translation import pgettext_lazy

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from utility.models import (BaseModel, BaseModelAdmin,
                            ManagerEnabled, ManagerDisabled)


class CommandsOutput(BaseModel):
    """
    CommandsOutput
    """
    command = models.ForeignKey(to='remotes.Command',
                                on_delete=models.CASCADE,
                                verbose_name=pgettext_lazy(
                                    'CommandsOutput',
                                    'command'))
    host = models.ForeignKey(to='remotes.Host',
                             on_delete=models.CASCADE,
                             verbose_name=pgettext_lazy(
                                 'CommandsOutput',
                                 'host'))
    output = models.TextField(blank=True,
                              null=True,
                              verbose_name=pgettext_lazy(
                                  'CommandsOutput',
                                  'output'))
    result = models.TextField(blank=True,
                              null=True,
                              verbose_name=pgettext_lazy(
                                  'CommandsOutput',
                                  'result'))
    timestamp = models.DateTimeField(blank=True,
                                     null=True,
                                     auto_now_add=True,
                                     verbose_name=pgettext_lazy(
                                         'CommandsOutput',
                                         'timestamp'))

    # Set the managers for the model
    objects = models.Manager()
    objects_enabled = ManagerEnabled()
    objects_disabled = ManagerDisabled()

    class Meta:
        # Define the database table
        ordering = ['timestamp', 'command_id']
        verbose_name = pgettext_lazy('CommandsOutput',
                                     'Commands output')
        verbose_name_plural = pgettext_lazy('CommandsOutput',
                                            'Commands outputs')

    def __str__(self):
        return f'{self.timestamp}'


class CommandsOutputAdmin(BaseModelAdmin):
    list_display = ('timestamp', 'command_name', 'group', 'host')
    list_filter = (('command__group', RelatedDropdownFilter),
                   ('command', RelatedDropdownFilter),
                   'command__group__hosts',
                   ('host', RelatedDropdownFilter))

    # noinspection PyMethodMayBeStatic
    def command_name(self, instance) -> int:
        """
        Return the associated command name

        :param instance: CommandsOutput instance
        :return: command name
        """
        return instance.command.name

    # noinspection PyMethodMayBeStatic
    def group(self, instance) -> 'models.CommandsGroup':
        """
        Return the associated command group item group

        :param instance: CommandsOutput instance
        :return: CommandsGroup object
        """
        return instance.command.group
