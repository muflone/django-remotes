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

from django.contrib import admin

from .constants import (ADMIN_SITE_HEADER,
                        ADMIN_SITE_INDEX_TITLE,
                        ADMIN_SITE_TITLE)
from .models import (ApiLog, ApiLogAdmin,
                     Command, CommandAdmin,
                     CommandVariable, CommandVariableAdmin,
                     CommandsGroup, CommandsGroupAdmin,
                     CommandsOutput, CommandsOutputAdmin,
                     Host, HostAdmin,
                     HostsGroup, HostsGroupAdmin,
                     Setting, SettingAdmin,
                     Variable, VariableAdmin,
                     VariableValue, VariableValueAdmin)

admin.site.site_header = ADMIN_SITE_HEADER
admin.site.site_title = ADMIN_SITE_TITLE
admin.site.index_title = ADMIN_SITE_INDEX_TITLE

admin.site.register(ApiLog, ApiLogAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(CommandVariable, CommandVariableAdmin)
admin.site.register(CommandsGroup, CommandsGroupAdmin)
admin.site.register(CommandsOutput, CommandsOutputAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(HostsGroup, HostsGroupAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Variable, VariableAdmin)
admin.site.register(VariableValue, VariableValueAdmin)
