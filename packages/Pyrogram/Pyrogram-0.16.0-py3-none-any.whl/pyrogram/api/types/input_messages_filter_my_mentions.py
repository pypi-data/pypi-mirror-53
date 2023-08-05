# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.api.core import *


class InputMessagesFilterMyMentions(TLObject):
    """Attributes:
        LAYER: ``105``

    Attributes:
        ID: ``0xc1f8e69a``

    No parameters required.
    """

    __slots__ = []

    ID = 0xc1f8e69a
    QUALNAME = "types.InputMessagesFilterMyMentions"

    def __init__(self, ):
        pass

    @staticmethod
    def read(b: BytesIO, *args) -> "InputMessagesFilterMyMentions":
        # No flags
        
        return InputMessagesFilterMyMentions()

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
