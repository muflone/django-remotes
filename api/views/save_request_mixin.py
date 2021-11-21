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

from remotes.models.request import Request


class SaveRequestMixin(object):
    def save_request(self, request, *args, **kwargs) -> None:
        Request.objects.create(
            username=request.user.username if request.user.pk else None,
            remote_address=request.META['REMOTE_ADDR'],
            method=request.META['REQUEST_METHOD'],
            path_info=request.META['PATH_INFO'],
            querystring=request.META['QUERY_STRING'])
