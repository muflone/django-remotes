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

ACTION_DISCOVER = 'discover'
ACTION_GENERATE_KEYS = 'generate_keys'
ACTION_STATUS = 'status'
ACTION_HOST_REGISTER = 'host_register'
ACTION_HOST_VERIFY = 'host_verify'

ACTIONS = (ACTION_DISCOVER,
           ACTION_GENERATE_KEYS,
           ACTION_STATUS,
           ACTION_HOST_REGISTER,
           ACTION_HOST_VERIFY)
