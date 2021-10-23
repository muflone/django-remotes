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

from remotes.client.keys import Keys
from remotes.constants import ENCRYPTED_FIELD
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
        # Obtain the host public key to encrypt the data
        keys = Keys()
        keys.load_public_key(data=host.pubkey)
        # Encrypt any field listed in encrypted_fields
        if self.encrypted_fields:
            results.data[ENCRYPTED_FIELD] = []
        for field in self.encrypted_fields:
            if field in results.data:
                # Encrypt the data
                results.data[field] = keys.encrypt(text=results.data[field],
                                                   use_base64=True)
                results.data[ENCRYPTED_FIELD].append(field)
        return results
