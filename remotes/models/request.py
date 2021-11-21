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

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import pgettext_lazy

from utility.models import BaseModel, BaseModelAdmin


class Request(BaseModel):
    """
    Request
    """
    timestamp = models.DateTimeField(auto_now_add=True,
                                     verbose_name=pgettext_lazy(
                                         'Request',
                                         'timestamp'))
    user = models.ForeignKey(to=get_user_model(),
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             default=None,
                             verbose_name=pgettext_lazy(
                                 'Request',
                                 'user'))
    remote_address = models.CharField(max_length=255,
                                      verbose_name=pgettext_lazy(
                                          'Request',
                                          'remote address'))
    method = models.CharField(max_length=255,
                              verbose_name=pgettext_lazy(
                                  'Request',
                                  'method'))
    path_info = models.CharField(max_length=255,
                                 verbose_name=pgettext_lazy(
                                     'Request',
                                     'path info'))
    querystring = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy(
                                       'Request',
                                       'query string'))

    class Meta:
        # Define the database table
        ordering = ['timestamp', 'id']
        verbose_name = pgettext_lazy('Request',
                                     'Request')
        verbose_name_plural = pgettext_lazy('Request',
                                            'Requests')

    def __str__(self):
        return f'{self.timestamp}'


class RequestAdmin(BaseModelAdmin):
    list_display = ('timestamp', 'user', 'remote_address', 'method',
                    'path_info')
    list_filter = ('user', 'remote_address', 'method', 'path_info')
    ordering = ['timestamp']
