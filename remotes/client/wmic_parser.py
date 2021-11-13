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

import subprocess
from typing import Optional, Union


class WmicParser(object):
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def get(self,
            role: str,
            field: str,
            condition: str = None) -> Optional[str]:
        """
        Get a single string item from wmic for the specified role
        :param role: WMI role alias to use
        :param field: single field to return
        :param condition: a condition to filter results
        :return: a single resulting value
        """
        values = self.get_values(role=role, fields=field, condition=condition)
        return values[0][field] if values else None

    def get_values(self,
                   role: str,
                   fields: Optional[Union[str, list, tuple]] = None,
                   condition: str = None
                   ) -> list[dict[str]]:
        """
        Get a list of items from wmic for the specified role
        :param role: WMI role alias to use
        :param fields: field list to return
        :param condition: a condition to filter results
        :return: a list of dictionary with items
        """
        results = []
        # Prepare arguments
        arguments = ['wmic', role]
        # Get condition
        if condition:
            arguments.append('WHERE')
            arguments.append(condition)
        arguments.append('GET')
        # Get fields
        if not fields:
            # Get all fields
            arguments.append('*')
        elif isinstance(fields, list) or isinstance(fields, tuple):
            # Fields list or tuple
            arguments.append(','.join(fields))
        else:
            # Field list as a string
            arguments.append(fields)
        arguments.append('/VALUE')
        process = subprocess.run(args=arguments,
                                 capture_output=True,
                                 timeout=self.timeout)
        item = {}
        for line in process.stdout.decode('utf-8').split('\n'):
            line = line.strip()
            # New item for empty lines
            if not line:
                # Save last result
                if item:
                    results.append(item)
                # Create new empty item
                item = {}
            elif '=' in line:
                # Split field
                name, value = line.split('=', 1)
                item[name] = value
        return results
