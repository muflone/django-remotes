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
    group_item = models.ForeignKey(to='remotes.CommandsGroupItem',
                                   on_delete=models.CASCADE,
                                   verbose_name=pgettext_lazy(
                                       'CommandsOutput',
                                       'group item'))
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
        ordering = ['timestamp', 'group_item_id']
        verbose_name = pgettext_lazy('CommandsOutput',
                                     'Commands output')
        verbose_name_plural = pgettext_lazy('CommandsOutput',
                                            'Commands outputs')

    def __str__(self):
        return f'{self.timestamp}'


class CommandsOutputAdmin(BaseModelAdmin):
    list_display = ('timestamp', 'item_id', 'group', 'command', 'host')
    list_filter = (('group_item__group', RelatedDropdownFilter),
                   ('group_item', RelatedDropdownFilter),
                   'group_item__group__hosts',
                   ('host', RelatedDropdownFilter))

    def item_id(self, instance) -> int:
        """
        Return the associated command group item ID
        :param instance: CommandsGroupItemVariable instance
        :return: command group item ID
        """
        return instance.group_item.id

    def group(self, instance) -> 'models.CommandsGroup':
        """
        Return the associated command group item group
        :param instance: CommandsGroupItemVariable instance
        :return: CommandsGroup object
        """
        return instance.group_item.group

    def command(self, instance) -> 'models.Command':
        """
        Return the associated command group item group
        :param instance: CommandsGroupItemVariable instance
        :return: Command object
        """
        return instance.group_item.command
