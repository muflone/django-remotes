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


class CommandsGroupItemVariable(BaseModel):
    """
    Variables with order for hosts
    """
    command_group_item = models.ForeignKey('remotes.CommandsGroupItem',
                                           on_delete=models.CASCADE,
                                           verbose_name=pgettext_lazy(
                                               'CommandsGroupItemVariable',
                                               'command group item'))
    variable = models.ForeignKey('remotes.Variable',
                                 on_delete=models.CASCADE,
                                 verbose_name=pgettext_lazy(
                                     'CommandsGroupItemVariable',
                                     'variable'))
    order = models.PositiveIntegerField(default=1,
                                        verbose_name=pgettext_lazy(
                                            'CommandsGroupItemVariable',
                                            'order'))

    # Set the managers for the model
    objects = models.Manager()
    objects_enabled = ManagerEnabled()
    objects_disabled = ManagerDisabled()

    class Meta:
        # Define the database table
        ordering = ['command_group_item', 'order', 'variable']
        unique_together = ('command_group_item', 'order')
        verbose_name = pgettext_lazy('CommandsGroupItemVariable',
                                     'Command group items variable')
        verbose_name_plural = pgettext_lazy('CommandsGroupItemVariable',
                                            'Commands group items variables')

    def __str__(self):
        return f'{self.command_group_item} - {self.order} - {self.variable}'


class CommandsGroupItemVariableAdmin(BaseModelAdmin):
    list_display = ('item_id',
                    'group',
                    'command',
                    'item_order',
                    'order',
                    'variable')
    list_filter = (('command_group_item__group', RelatedDropdownFilter),
                   ('command_group_item__command', RelatedDropdownFilter),
                   ('variable', RelatedDropdownFilter),
                   ('command_group_item__group__hosts', RelatedDropdownFilter))

    # noinspection PyMethodMayBeStatic
    def item_id(self, instance) -> int:
        """
        Return the associated command group item ID
        :param instance: CommandsGroupItemVariable instance
        :return: command group item ID
        """
        return instance.command_group_item.id

    # noinspection PyMethodMayBeStatic
    def item_order(self, instance) -> int:
        """
        Return the associated command group item order
        :param instance: CommandsGroupItemVariable instance
        :return: command group item order
        """
        return instance.command_group_item.order

    # noinspection PyMethodMayBeStatic
    def group(self, instance) -> 'models.CommandsGroup':
        """
        Return the associated command group item group
        :param instance: CommandsGroupItemVariable instance
        :return: CommandsGroup object
        """
        return instance.command_group_item.group

    # noinspection PyMethodMayBeStatic
    def command(self, instance) -> 'models.Command':
        """
        Return the associated command group item group
        :param instance: CommandsGroupItemVariable instance
        :return: Command object
        """
        return instance.command_group_item.command
