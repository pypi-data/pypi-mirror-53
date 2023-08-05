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


class UpdateReadChannelInbox(TLObject):
    """Attributes:
        LAYER: ``105``

    Attributes:
        ID: ``0x330b5424``

    Parameters:
        channel_id: ``int`` ``32-bit``
        max_id: ``int`` ``32-bit``
        still_unread_count: ``int`` ``32-bit``
        pts: ``int`` ``32-bit``
        folder_id (optional): ``int`` ``32-bit``
    """

    __slots__ = ["channel_id", "max_id", "still_unread_count", "pts", "folder_id"]

    ID = 0x330b5424
    QUALNAME = "types.UpdateReadChannelInbox"

    def __init__(self, *, channel_id: int, max_id: int, still_unread_count: int, pts: int, folder_id: int = None):
        self.folder_id = folder_id  # flags.0?int
        self.channel_id = channel_id  # int
        self.max_id = max_id  # int
        self.still_unread_count = still_unread_count  # int
        self.pts = pts  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateReadChannelInbox":
        flags = Int.read(b)
        
        folder_id = Int.read(b) if flags & (1 << 0) else None
        channel_id = Int.read(b)
        
        max_id = Int.read(b)
        
        still_unread_count = Int.read(b)
        
        pts = Int.read(b)
        
        return UpdateReadChannelInbox(channel_id=channel_id, max_id=max_id, still_unread_count=still_unread_count, pts=pts, folder_id=folder_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.folder_id is not None else 0
        b.write(Int(flags))
        
        if self.folder_id is not None:
            b.write(Int(self.folder_id))
        
        b.write(Int(self.channel_id))
        
        b.write(Int(self.max_id))
        
        b.write(Int(self.still_unread_count))
        
        b.write(Int(self.pts))
        
        return b.getvalue()
