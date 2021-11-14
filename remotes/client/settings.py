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

import configparser
import urllib.parse

from remotes.constants import SERVER_URL


SECTION_ENDPOINTS = 'endpoints'
SECTION_HOST = 'host'
SECTION_SERVER = 'server'

OPTION_PRIVATE_KEY = 'private_key'
OPTION_PUBLIC_KEY = 'public_key'
OPTION_TOKEN = 'token'


class Settings(object):
    def __init__(self):
        self.settings = configparser.RawConfigParser()

    def load(self, filename: str):
        """
        Load the settings file

        :param filename: file to load settings from
        :return: None
        """
        self.settings.read(filenames=filename)

    def save(self, filename: str):
        """
        Save settings to file
        :return: None
        """
        with open(file=filename, mode='w') as file:
            self.settings.write(file)

    def get_value(self, section: str, option: str):
        """
        Get a value from an option

        :param section: section in settings
        :param option: option name
        :return: value
        """
        results = None
        if section in self.settings.sections():
            results = self.settings.get(section=section,
                                        option=option,
                                        fallback=None)
        return results

    def set_value(self, section: str, option: str, value: str):
        """
        Save a value to an option

        :param section: section in settings
        :param option: option name
        :param value: value
        :return: None
        """
        if section not in self.settings.sections():
            self.settings.add_section(section)
        self.settings.set(section=section,
                          option=option,
                          value=value)

    def build_url(self, url: str, extra: str = None) -> str:
        """
        Build URL using the server_url and the url

        :param url: additional URL
        :param extra: additional URL path
        :return: full URL
        """
        results = urllib.parse.urljoin(
            base=self.get_value(section=SECTION_SERVER,
                                option=SERVER_URL),
            url=url)
        return (results
                if not extra
                else f'{results}{extra}')
