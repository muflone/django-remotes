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

ACTION_COMMAND_GET = 'command_get'
ACTION_COMMAND_POST = 'command_post'
ACTION_COMMANDS_LIST = 'commands_list'
ACTION_COMMANDS_PROCESS = 'commands_process'
ACTION_DISCOVER = 'discover'
ACTION_GENERATE_KEYS = 'generate_keys'
ACTION_HOST_REGISTER = 'host_register'
ACTION_HOST_VERIFY = 'host_verify'
ACTION_NEW_HOST = 'new_host'
ACTION_STATUS = 'status'

ACTIONS = (ACTION_COMMAND_GET,
           ACTION_COMMAND_POST,
           ACTION_COMMANDS_LIST,
           ACTION_COMMANDS_PROCESS,
           ACTION_DISCOVER,
           ACTION_GENERATE_KEYS,
           ACTION_HOST_REGISTER,
           ACTION_HOST_VERIFY,
           ACTION_NEW_HOST,
           ACTION_STATUS)
