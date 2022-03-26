##
#     Project: Django Remotes
# Description: A Django application to execute remote commands
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021-2022 Fabio Castelli
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

import json
import sys

try:
    from remotes.client.client import Client                       # noqa: F401
except ModuleNotFoundError:
    # Fix module search path adding the current directory
    # Mostly needed for embedded Python
    sys.path.append('.')
    from remotes.client.client import Client


def main():
    client = Client()
    # Get command line arguments
    client.get_command_line()
    # Load settings
    client.load()
    # Process the arguments
    process_status, process_results = client.process()
    if process_results is not None:
        # Show the results
        print(json.dumps(process_results, indent=2)
              if process_results
              else None)
    # Save settings
    client.save()
    # Set exit code accordingly to the executed action
    sys.exit(process_status)


if __name__ == '__main__':
    main()
