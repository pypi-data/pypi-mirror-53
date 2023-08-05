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


class StickerSetCovered(TLObject):
    """Attributes:
        LAYER: ``105``

    Attributes:
        ID: ``0x6410a5d2``

    Parameters:
        set: :obj:`StickerSet <pyrogram.api.types.StickerSet>`
        cover: Either :obj:`DocumentEmpty <pyrogram.api.types.DocumentEmpty>` or :obj:`Document <pyrogram.api.types.Document>`

    See Also:
        This object can be returned by :obj:`messages.GetAttachedStickers <pyrogram.api.functions.messages.GetAttachedStickers>`.
    """

    __slots__ = ["set", "cover"]

    ID = 0x6410a5d2
    QUALNAME = "types.StickerSetCovered"

    def __init__(self, *, set, cover):
        self.set = set  # StickerSet
        self.cover = cover  # Document

    @staticmethod
    def read(b: BytesIO, *args) -> "StickerSetCovered":
        # No flags
        
        set = TLObject.read(b)
        
        cover = TLObject.read(b)
        
        return StickerSetCovered(set=set, cover=cover)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.set.write())
        
        b.write(self.cover.write())
        
        return b.getvalue()
