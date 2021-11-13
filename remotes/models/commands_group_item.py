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

from django.contrib.admin import TabularInline
from django.db import models
from django.utils.translation import pgettext_lazy

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from utility.actions import ActionSetActive, ActionSetInactive
from utility.models import (BaseModel, BaseModelAdmin,
                            ManagerEnabled, ManagerDisabled)


class CommandsGroupItem(BaseModel):
    """
    CommandsGroupItem
    """
    group = models.ForeignKey(to='remotes.CommandsGroup',
                              on_delete=models.PROTECT,
                              verbose_name=pgettext_lazy(
                                  'CommandsGroupItem',
                                  'group'))
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name=pgettext_lazy(
                                       'CommandsGroupItem',
                                       'description'))
    command = models.ForeignKey(to='remotes.Command',
                                on_delete=models.PROTECT,
                                verbose_name=pgettext_lazy(
                                    'CommandsGroupItem',
                                    'command'))
    variables = models.ManyToManyField(
        to='remotes.Variable',
        through='remotes.CommandsGroupItemVariable',
        blank=True,
        verbose_name=pgettext_lazy(
            'CommandsGroupItem',
            'variables'))
    order = models.PositiveIntegerField(default=1,
                                        verbose_name=pgettext_lazy(
                                            'CommandsGroupItem',
                                            'order'))
    is_active = models.BooleanField(default=True,
                                    verbose_name=pgettext_lazy(
                                        'CommandsGroupItem',
                                        'active'))

    # Set the managers for the model
    objects = models.Manager()
    objects_enabled = ManagerEnabled()
    objects_disabled = ManagerDisabled()

    class Meta:
        # Define the database table
        ordering = ['group', 'order', '-is_active', 'command']
        verbose_name = pgettext_lazy('CommandsGroupItem',
                                     'Commands group item')
        verbose_name_plural = pgettext_lazy('CommandsGroupItem',
                                            'Commands group items')

    def __str__(self):
        return f'{self.group_id} - {self.group} - {self.command}'

    def group_order(self):
        """
        Return the group order
        :return: group order
        """
        return self.group.order


class CommandsGroupItemInline(TabularInline):
    model = CommandsGroupItem
    fields = ('command', 'order', 'is_active')


class CommandsGroupItemAdmin(BaseModelAdmin,
                             ActionSetActive,
                             ActionSetInactive):
    actions = ['set_active', 'set_inactive']
    list_display = ('id', 'group', 'command', 'order', 'is_active')
    list_filter = (('group', RelatedDropdownFilter),
                   ('command', RelatedDropdownFilter),
                   'is_active',
                   'group__hosts')
