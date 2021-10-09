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


class CommandQueue(BaseModel):
    """
    CommandQueue
    """
    hosts = models.ForeignKey(to='remotes.HostsGroup',
                              on_delete=models.PROTECT,
                              verbose_name=pgettext_lazy(
                                  'CommandQueue',
                                  'hosts'))
    name = models.CharField(max_length=255,
                            unique=True,
                            verbose_name=pgettext_lazy(
                                'CommandQueue',
                                'name'))
    command = models.ForeignKey(to='remotes.Command',
                                on_delete=models.PROTECT,
                                verbose_name=pgettext_lazy(
                                    'CommandQueue',
                                    'command'))
    variable = models.CharField(max_length=255,
                                blank=True,
                                null=False,
                                verbose_name=pgettext_lazy(
                                    'CommandQueue',
                                    'variable'))
    order = models.PositiveIntegerField(default=1,
                                        verbose_name=pgettext_lazy(
                                            'CommandQueue',
                                            'order'))
    after = models.DateTimeField(blank=True,
                                 null=True,
                                 verbose_name=pgettext_lazy(
                                     'CommandQueue',
                                     'after'))
    before = models.DateTimeField(blank=True,
                                  null=True,
                                  verbose_name=pgettext_lazy(
                                      'CommandQueue',
                                      'before'))
    is_active = models.BooleanField(default=True,
                                    verbose_name=pgettext_lazy(
                                        'CommandQueue',
                                        'active'))

    # Set the managers for the model
    objects = models.Manager()
    objects_enabled = ManagerEnabled()
    objects_disabled = ManagerDisabled()

    class Meta:
        # Define the database table
        ordering = ['hosts', 'order', '-is_active', 'command']
        verbose_name = pgettext_lazy('CommandQueue',
                                     'Command queue')
        verbose_name_plural = pgettext_lazy('CommandQueue',
                                            'Command queues')

    def __str__(self):
        return '{NAME}'.format(NAME=self.name)


class CommandQueueAdmin(BaseModelAdmin):
    list_display = ('hosts', 'name', 'order', 'after', 'before', 'is_active')
