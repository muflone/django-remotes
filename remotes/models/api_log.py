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

import datetime

from django.db import models
from django.utils.translation import pgettext_lazy

from django_admin_listfilter_dropdown.filters import DropdownFilter

from utility.models import BaseModel, BaseModelAdmin


class ApiLog(BaseModel):
    date = models.DateField(verbose_name=pgettext_lazy('ApiLog',
                                                       'date'))
    time = models.TimeField(verbose_name=pgettext_lazy('ApiLog',
                                                       'time'))
    message_level = models.PositiveIntegerField(verbose_name=pgettext_lazy(
        'ApiLog',
        'message level'))
    method = models.CharField(max_length=255,
                              verbose_name=pgettext_lazy('ApiLog',
                                                         'metod'))
    path = models.CharField(max_length=255,
                            verbose_name=pgettext_lazy('ApiLog',
                                                       'path'))
    raw_uri = models.TextField(blank=False,
                               verbose_name=pgettext_lazy('ApiLog',
                                                          'raw uri'))
    url_name = models.CharField(max_length=255,
                                verbose_name=pgettext_lazy('ApiLog',
                                                           'url name'))
    func_name = models.CharField(max_length=255,
                                 verbose_name=pgettext_lazy('ApiLog',
                                                            'function name'))
    remote_addr = models.CharField(max_length=255,
                                   blank=True,
                                   verbose_name=pgettext_lazy(
                                       'ApiLog',
                                       'remote address'))
    forwarded_for = models.CharField(max_length=255,
                                     blank=True,
                                     verbose_name=pgettext_lazy(
                                         'ApiLog',
                                         'forwarded for'))
    user_agent = models.CharField(max_length=255,
                                  blank=True,
                                  verbose_name=pgettext_lazy('ApiLog',
                                                             'user agent'))
    client_agent = models.CharField(max_length=255,
                                    blank=True,
                                    verbose_name=pgettext_lazy('ApiLog',
                                                               'client agent'))
    client_version = models.CharField(max_length=255,
                                      blank=True,
                                      verbose_name=pgettext_lazy(
                                          'ApiLog',
                                          'client version'))
    username = models.CharField(max_length=255,
                                blank=True,
                                verbose_name=pgettext_lazy('ApiLog',
                                                           'username'))
    args = models.TextField(blank=True,
                            verbose_name=pgettext_lazy('ApiLog',
                                                       'arguments'))
    kwargs = models.TextField(blank=True,
                              verbose_name=pgettext_lazy('ApiLog',
                                                         'keyword arguments'))
    extra = models.TextField(blank=True,
                             verbose_name=pgettext_lazy('ApiLog',
                                                        'extra'))

    class Meta:
        # Define the database table
        db_table = 'api_log'
        ordering = ['-date', '-time', '-id']
        verbose_name = pgettext_lazy('ApiLog', 'Api log')
        verbose_name_plural = pgettext_lazy('ApiLog',
                                            'Api logs')

    def __str__(self):
        return str(self.pk)


class ApiLogAdmin(BaseModelAdmin):
    list_display = ('id', 'timestamp', 'username', 'remote_addr', 'method',
                    'path')
    list_filter = (('username', DropdownFilter),
                   ('remote_addr', DropdownFilter),
                   'method',
                   ('url_name', DropdownFilter),
                   'client_agent',
                   'client_version')
    ordering = ['date', 'time', 'id']

    def timestamp(self, instance):
        return datetime.datetime.combine(instance.date, instance.time)
