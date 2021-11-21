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
import json

from remotes.models.api_log import ApiLog


class SaveRequestMixin(object):
    def save_request(self, request, *args, **kwargs) -> None:
        ApiLog.objects.create(
            date=datetime.date.today(),
            time=datetime.datetime.now().replace(microsecond=0),
            message_level=0,
            method=request.method,
            path=request.path,
            raw_uri=request.get_raw_uri(),
            url_name=request.resolver_match.url_name,
            func_name=request.resolver_match.func.__name__,
            remote_addr=request.META.get('REMOTE_ADDR', ''),
            forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            client_agent=request.META.get('HTTP_CLIENT_AGENT', ''),
            client_version=request.META.get('HTTP_CLIENT_VERSION', ''),
            username=request.user,
            args=self.json_prettify(args),
            kwargs=self.json_prettify(kwargs),
            extra='')

    def json_prettify(self, arguments):
        """Format the arguments in JSON formatted style"""
        return (json.dumps(arguments, sort_keys=False, indent=2)
                if arguments else '')
