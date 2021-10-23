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

from rest_framework.generics import RetrieveAPIView

from remotes.models import Host


class RetrieveAPIEncryptedView(RetrieveAPIView):
    """
    RetrieveAPI implementation which encrypts the fields listed in
    `encrypted_fields` using the host public key
    """
    encrypted_fields = []

    def get(self, request, *args, **kwargs):
        results = super().get(request, *args, **kwargs)
        # Get host for the current user
        host = Host.objects.get(user=self.request.user)
        host.encrypt_data(data=results.data, fields=self.encrypted_fields)
        return results
