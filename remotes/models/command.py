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

from utility.actions import (ActionOrderIncrease,
                             ActionSetActive,
                             ActionSetInactive)
from utility.models import (BaseModel, BaseModelAdmin,
                            ManagerEnabled, ManagerDisabled)


class Command(BaseModel):
    """
    Command
    """
    name = models.CharField(max_length=255,
                            blank=False,
                            null=False,
                            verbose_name=pgettext_lazy(
                                'Command',
                                'name'))
    group = models.ForeignKey(to='remotes.CommandsGroup',
                              on_delete=models.PROTECT,
                              verbose_name=pgettext_lazy(
                                  'Command',
                                  'group'))
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name=pgettext_lazy(
                                       'Command',
                                       'description'))
    settings = models.ManyToManyField(blank=True,
                                      to='remotes.Setting',
                                      verbose_name=pgettext_lazy(
                                          'Command',
                                          'input settings'))
    variables = models.ManyToManyField(blank=True,
                                       to='remotes.Variable',
                                       verbose_name=pgettext_lazy(
                                           'Command',
                                           'input variables'))
    command = models.TextField(verbose_name=pgettext_lazy(
                                   'Command',
                                   'command'))
    output_variables = models.ManyToManyField(
        to='remotes.Variable',
        related_name='output_variables_set',
        through='remotes.CommandVariable',
        blank=True,
        verbose_name=pgettext_lazy('Command',
                                   'output variables'))
    timeout = models.PositiveIntegerField(default=15,
                                          verbose_name=pgettext_lazy(
                                              'Command',
                                              'timeout'))
    order = models.PositiveIntegerField(default=1,
                                        verbose_name=pgettext_lazy(
                                            'Command',
                                            'order'))
    is_active = models.BooleanField(default=True,
                                    verbose_name=pgettext_lazy(
                                        'Command',
                                        'active'))

    # Set the managers for the model
    objects = models.Manager()
    objects_enabled = ManagerEnabled()
    objects_disabled = ManagerDisabled()

    class Meta:
        # Define the database table
        ordering = ['group', 'order', '-is_active']
        unique_together = (('name', 'group'))
        verbose_name = pgettext_lazy('Command',
                                     'Command')
        verbose_name_plural = pgettext_lazy('Command',
                                            'Commands')

    def __str__(self):
        return self.name

    def group_order(self):
        """
        Return the group order
        :return: group order
        """
        return self.group.order


class CommandInline(TabularInline):
    model = Command
    fields = ('name', 'order', 'command', 'is_active')


class CommandAdmin(BaseModelAdmin,
                   ActionOrderIncrease,
                   ActionSetActive,
                   ActionSetInactive):
    actions = ['order_increase', 'set_active', 'set_inactive']
    list_display = ('id', 'name', 'group', 'order', 'description', 'is_active')
    list_filter = (('group', RelatedDropdownFilter),
                   'is_active',
                   'group__hosts')
