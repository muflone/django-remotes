##
#     Project: Django Remotes
# Description: A Django application to execute remote commands
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021-2022 Fabio Castelli
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

from utility.actions import ActionOrderDecrease, ActionOrderIncrease
from utility.models import (BaseModel, BaseModelAdmin,
                            ManagerEnabled, ManagerDisabled)


class CommandVariable(BaseModel):
    """
    Variables with order for hosts
    """
    command = models.ForeignKey('remotes.Command',
                                on_delete=models.CASCADE,
                                verbose_name=pgettext_lazy(
                                    'CommandVariable',
                                    'command'))
    variable = models.ForeignKey('remotes.Variable',
                                 on_delete=models.CASCADE,
                                 verbose_name=pgettext_lazy(
                                     'CommandVariable',
                                     'variable'))
    order = models.PositiveIntegerField(default=0,
                                        verbose_name=pgettext_lazy(
                                            'CommandVariable',
                                            'order'))

    # Set the managers for the model
    objects = models.Manager()
    objects_enabled = ManagerEnabled()
    objects_disabled = ManagerDisabled()

    class Meta:
        # Define the database table
        ordering = ['command', 'order', 'variable']
        unique_together = ('command', 'order', 'variable')
        verbose_name = pgettext_lazy('CommandVariable',
                                     'Command variable')
        verbose_name_plural = pgettext_lazy('CommandVariable',
                                            'Commands variables')

    def __str__(self):
        return f'{self.command} - {self.order} - {self.variable}'


class CommandVariableAdmin(BaseModelAdmin,
                           ActionOrderDecrease,
                           ActionOrderIncrease):
    actions = ['order_decrease', 'order_increase']
    list_display = ('command_id',
                    'group',
                    'command',
                    'command_order',
                    'order',
                    'variable')
    list_filter = (('command__group', RelatedDropdownFilter),
                   ('command', RelatedDropdownFilter),
                   ('variable', RelatedDropdownFilter),
                   ('command__group__hosts', RelatedDropdownFilter))

    # noinspection PyMethodMayBeStatic
    def command_id(self, instance) -> int:
        """
        Return the associated command ID

        :param instance: CommandVariable instance
        :return: command ID
        """
        return instance.command.pk

    # noinspection PyMethodMayBeStatic
    def command_order(self, instance) -> int:
        """
        Return the associated command order

        :param instance: CommandVariable instance
        :return: command order
        """
        return instance.command.order

    # noinspection PyMethodMayBeStatic
    def group(self, instance) -> 'models.CommandsGroup':
        """
        Return the associated command group

        :param instance: CommandVariable instance
        :return: CommandsGroup object
        """
        return instance.command.group
