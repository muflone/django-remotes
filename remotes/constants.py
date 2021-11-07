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

SERVER_URL = 'server_url'
API_VERSION = 'v1'

MESSAGE_FIELD = 'message'

STATUS_FIELD = 'status'
STATUS_OK = 'OK'
STATUS_ERROR = 'ERROR'

ENCRYPTED_FIELD = 'encrypted'
ENDPOINTS_FIELD = 'endpoints'
ENCRYPTION_KEY_FIELD = 'encryption_key'
PUBLIC_KEY_FIELD = 'public_key'
UUID_FIELD = 'uuid'

HOSTS_GROUP_AUTO_ADD = 'hosts_group_auto_add'
USER_GROUP_REGISTER_HOSTS = 'user_register_hosts'

PERMISSION_CAN_REGISTER_HOSTS = 'can_register_hosts'
PERMISSION_CAN_REGISTER_HOSTS_FULL = f'auth.{PERMISSION_CAN_REGISTER_HOSTS}'

RESULTS_FIELD = 'results'
ID_FIELD = 'id'
USER_ID_FIELD = 'user_id'
USER_NAME_FIELD = 'user_name'
HOSTS_GROUPS = 'hosts_groups'
GROUP_FIELD = 'group'
COMMAND_FIELD = 'command'
COMMANDS_RESULTS_FIELD = 'commands_results'

METHOD_GET = 'get'
METHOD_POST = 'post'
