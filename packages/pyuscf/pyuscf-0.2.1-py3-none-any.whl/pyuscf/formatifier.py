# Copyright 2019 Juan Antonio Sauceda <jasgordo@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""Formatifier class, mainly use to provide different output views."""

import json

__license__ = 'GNU General Public License v2.0'


class Formatify(object):
    """The Formatify class.

    The Formatify class is used to convert a list of dict(s) to multiple
    different views.

    Args:
        iterable (dict): A list of dict(s).

    Attributes:
        iterable (dict): A list of dict(s).
    """

    def __init__(self, iterable=None):
        self.iterable = iterable

    def __str__(self):
        """Overwrite of the built in str type."""

        return self.string_modifier(self.iterable)

    @staticmethod
    def string_modifier(obj, newline=' '):
        """A string function modifier for the use of __str__.

        Args:
            obj (dict): A list of dict(s).
            newline (str): A newline char. default ' '.

        Returns:
            A string with chosen newline char.
        """

        data = ''
        for elm in obj:
            for key, value in elm.items():
                data += key + " = " + value + newline
        return data

    def to_csv(self):
        """To comma seperated value (csv).

        Returns:
            A string in the format of csv.
        """

        keys = ""
        values = ""
        for elm in self.iterable:
            for key, value in elm.items():
                keys += '"' + key + '",'
                values += '"' + value + '",'
        return keys.rstrip(',') + '\n' + values.rstrip(',')

    def to_lines(self):
        """To lines with newline char.

        Returns:
            A string with newline char.
        """

        return self.string_modifier(self.iterable, newline='\n')

    def to_json(self):
        """To JavaScript Object Notation (JSON).

        Returns:
            A string as a JSON.
        """

        return json.dumps(self.iterable)
