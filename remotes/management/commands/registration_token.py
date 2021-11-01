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

import sys

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from rest_framework.authtoken.models import Token

from remotes.constants import USER_GROUP_REGISTER_HOSTS


class Command(BaseCommand):
    help = 'Get the registration token'

    def handle(self, *args, **options) -> None:
        """
        Get the registration token
        """
        group = Group.objects.filter(name=USER_GROUP_REGISTER_HOSTS).first()
        if group:
            token = Token.objects.filter(user=group.user_set.first()).first()
            if token:
                print('You can use the following token to register new hosts:',
                      token)
            else:
                # Missing users
                print(f'No users set for group {USER_GROUP_REGISTER_HOSTS}')
                sys.exit(2)
        else:
            # Missing group
            print(f'Missing group {USER_GROUP_REGISTER_HOSTS}')
            sys.exit(1)