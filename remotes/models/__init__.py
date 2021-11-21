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

from .api_log import ApiLog, ApiLogAdmin                           # noqa: F401
from .command import Command, CommandAdmin                         # noqa: F401
from .command_variable import (CommandVariable,                    # noqa: F401
                               CommandVariableAdmin)               # noqa: F401
from .commands_group import CommandsGroup, CommandsGroupAdmin      # noqa: F401
from .commands_output import CommandsOutput, CommandsOutputAdmin   # noqa: F401
from .host import Host, HostAdmin                                  # noqa: F401
from .hostsgroup import HostsGroup, HostsGroupAdmin                # noqa: F401
from .setting import Setting, SettingAdmin                         # noqa: F401
from .variable import Variable, VariableAdmin                      # noqa: F401
from .variable_value import VariableValue, VariableValueAdmin      # noqa: F401
