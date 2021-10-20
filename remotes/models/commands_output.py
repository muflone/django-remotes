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


class CommandsOutput(BaseModel):
    """
    CommandsOutput
    """
    host = models.ForeignKey(to='remotes.Host',
                             on_delete=models.PROTECT,
                             verbose_name=pgettext_lazy(
                                 'CommandsOutput',
                                 'host'))
    command = models.ForeignKey(to='remotes.Command',
                                on_delete=models.PROTECT,
                                verbose_name=pgettext_lazy(
                                    'CommandsOutput',
                                    'command'))
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
                                     verbose_name=pgettext_lazy(
                                         'CommandsOutput',
                                         'timestamp'))

    # Set the managers for the model
    objects = models.Manager()
    objects_enabled = ManagerEnabled()
    objects_disabled = ManagerDisabled()

    class Meta:
        # Define the database table
        ordering = ['timestamp', 'host', 'command']
        verbose_name = pgettext_lazy('CommandsOutput',
                                     'Commands output')
        verbose_name_plural = pgettext_lazy('CommandsOutput',
                                            'Commands outputs')

    def __str__(self):
        return '{TIMESTAMP}'.format(TIMESTAMP=self.timestamp)


class CommandsOutputAdmin(BaseModelAdmin):
    list_display = ('timestamp', 'host', 'command')
