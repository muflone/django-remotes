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

from remotes.models.commands_group_item import CommandsGroupItemInline

from utility.actions import ActionSetActive, ActionSetInactive
from utility.models import (BaseModel, BaseModelAdmin,
                            ManagerEnabled, ManagerDisabled)


class CommandsGroup(BaseModel):
    """
    CommandsGroup
    """
    hosts = models.ForeignKey(to='remotes.HostsGroup',
                              on_delete=models.PROTECT,
                              verbose_name=pgettext_lazy(
                                  'CommandsGroup',
                                  'hosts'))
    name = models.CharField(max_length=255,
                            unique=True,
                            verbose_name=pgettext_lazy(
                                'CommandsGroup',
                                'name'))
    order = models.PositiveIntegerField(default=1,
                                        unique=True,
                                        verbose_name=pgettext_lazy(
                                            'CommandsGroup',
                                            'order'))
    after = models.DateTimeField(blank=False,
                                 null=False,
                                 verbose_name=pgettext_lazy(
                                     'CommandsGroup',
                                     'after'))
    before = models.DateTimeField(blank=False,
                                  null=False,
                                  verbose_name=pgettext_lazy(
                                      'CommandsGroup',
                                      'before'))
    is_active = models.BooleanField(default=True,
                                    verbose_name=pgettext_lazy(
                                        'CommandsGroup',
                                        'active'))

    # Set the managers for the model
    objects = models.Manager()
    objects_enabled = ManagerEnabled()
    objects_disabled = ManagerDisabled()

    class Meta:
        # Define the database table
        ordering = ['order', 'hosts', 'name', '-is_active']
        verbose_name = pgettext_lazy('CommandsGroup',
                                     'Commands group')
        verbose_name_plural = pgettext_lazy('CommandsGroup',
                                            'Commands groups')

    def __str__(self):
        return self.name


class CommandsGroupAdmin(BaseModelAdmin,
                         ActionSetActive,
                         ActionSetInactive):
    actions = ['set_active', 'set_inactive']
    inlines = [CommandsGroupItemInline]
    list_display = ('order', 'hosts', 'name', 'after', 'before', 'is_active')
    list_filter = ('hosts', 'is_active')
