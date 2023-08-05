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


class UpdateBotCallbackQuery(TLObject):
    """Attributes:
        LAYER: ``105``

    Attributes:
        ID: ``0xe73547e1``

    Parameters:
        query_id: ``int`` ``64-bit``
        user_id: ``int`` ``32-bit``
        peer: Either :obj:`PeerUser <pyrogram.api.types.PeerUser>`, :obj:`PeerChat <pyrogram.api.types.PeerChat>` or :obj:`PeerChannel <pyrogram.api.types.PeerChannel>`
        msg_id: ``int`` ``32-bit``
        chat_instance: ``int`` ``64-bit``
        data (optional): ``bytes``
        game_short_name (optional): ``str``
    """

    __slots__ = ["query_id", "user_id", "peer", "msg_id", "chat_instance", "data", "game_short_name"]

    ID = 0xe73547e1
    QUALNAME = "types.UpdateBotCallbackQuery"

    def __init__(self, *, query_id: int, user_id: int, peer, msg_id: int, chat_instance: int, data: bytes = None, game_short_name: str = None):
        self.query_id = query_id  # long
        self.user_id = user_id  # int
        self.peer = peer  # Peer
        self.msg_id = msg_id  # int
        self.chat_instance = chat_instance  # long
        self.data = data  # flags.0?bytes
        self.game_short_name = game_short_name  # flags.1?string

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateBotCallbackQuery":
        flags = Int.read(b)
        
        query_id = Long.read(b)
        
        user_id = Int.read(b)
        
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        chat_instance = Long.read(b)
        
        data = Bytes.read(b) if flags & (1 << 0) else None
        game_short_name = String.read(b) if flags & (1 << 1) else None
        return UpdateBotCallbackQuery(query_id=query_id, user_id=user_id, peer=peer, msg_id=msg_id, chat_instance=chat_instance, data=data, game_short_name=game_short_name)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.data is not None else 0
        flags |= (1 << 1) if self.game_short_name is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.query_id))
        
        b.write(Int(self.user_id))
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        b.write(Long(self.chat_instance))
        
        if self.data is not None:
            b.write(Bytes(self.data))
        
        if self.game_short_name is not None:
            b.write(String(self.game_short_name))
        
        return b.getvalue()
