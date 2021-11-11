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

from utility.models import (BaseModel, BaseModelAdmin,
                            ManagerEnabled, ManagerDisabled)


class CommandsGroupItemVariable(BaseModel):
    """
    Variables with order for hosts
    """
    command_group_item = models.ForeignKey('remotes.CommandsGroupItem',
                                           on_delete=models.PROTECT,
                                           verbose_name=pgettext_lazy(
                                               'CommandsGroupItemVariable',
                                               'command group item'))
    variable = models.ForeignKey('remotes.Variable',
                                 on_delete=models.PROTECT,
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
    list_display = ('command_group_item', 'variable', 'order')
    list_filter = (('variable', ))
