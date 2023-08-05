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


class InputStickeredMediaDocument(TLObject):
    """Attributes:
        LAYER: ``105``

    Attributes:
        ID: ``0x0438865b``

    Parameters:
        id: Either :obj:`InputDocumentEmpty <pyrogram.api.types.InputDocumentEmpty>` or :obj:`InputDocument <pyrogram.api.types.InputDocument>`
    """

    __slots__ = ["id"]

    ID = 0x0438865b
    QUALNAME = "types.InputStickeredMediaDocument"

    def __init__(self, *, id):
        self.id = id  # InputDocument

    @staticmethod
    def read(b: BytesIO, *args) -> "InputStickeredMediaDocument":
        # No flags
        
        id = TLObject.read(b)
        
        return InputStickeredMediaDocument(id=id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.id.write())
        
        return b.getvalue()
