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

"""The Unofficial USCF Member Service Area (MSA) API.

The United States Chess Federation (USCF) website for publicly available
chess member information. The package is nothing more than a client, but there
are some limitations on searching for chess members' information.

Visit www.uschess.org for further information on the limitations.
"""

from .msa import Msa
from .exception import IdTypeError
from .formatifier import Formatify

__author__ = 'Juan Antonio Sauceda <jasgordo@gmail.com>'
__version__ = '0.2.1'
__license__ = 'GNU General Public License v2.0'

__all__ = ['Msa', 'IdTypeError', 'Formatify']
