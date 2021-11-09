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

from utility.models import BaseModel, BaseModelAdmin


class VariableValue(BaseModel):
    """
    Variable
    """
    host = models.ForeignKey(to='remotes.Host',
                             on_delete=models.CASCADE,
                             verbose_name=pgettext_lazy(
                                 'VariableValue',
                                 'host'))
    variable = models.ForeignKey(to='remotes.Variable',
                                 on_delete=models.CASCADE,
                                 verbose_name=pgettext_lazy(
                                     'VariableValue',
                                     'variable'))
    value = models.TextField(blank=True,
                             null=False,
                             verbose_name=pgettext_lazy(
                                 'VariableValue',
                                 'value'))
    timestamp = models.DateTimeField(auto_now=True,
                                     verbose_name=pgettext_lazy(
                                         'VariableValue',
                                         'timestamp'))

    class Meta:
        # Define the database table
        unique_together = [('host', 'variable')]
        ordering = ['host', 'variable']
        verbose_name = pgettext_lazy('VariableValue',
                                     'Variable value')
        verbose_name_plural = pgettext_lazy('VariableValue',
                                            'Variable values')

    def __str__(self):
        return f'{self.host} - {self.variable}'


class VariableValueAdmin(BaseModelAdmin):
    list_display = ('host', 'variable', 'value', 'timestamp')
    list_filter = (('host', RelatedDropdownFilter),
                   'variable__category',
                   ('variable', RelatedDropdownFilter))
    readonly_fields = ('timestamp',)
