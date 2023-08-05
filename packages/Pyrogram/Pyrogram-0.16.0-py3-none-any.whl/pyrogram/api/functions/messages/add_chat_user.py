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


class AddChatUser(TLObject):
    """Attributes:
        LAYER: ``105``

    Attributes:
        ID: ``0xf9a0aa09``

    Parameters:
        chat_id: ``int`` ``32-bit``
        user_id: Either :obj:`InputUserEmpty <pyrogram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <pyrogram.api.types.InputUserSelf>`, :obj:`InputUser <pyrogram.api.types.InputUser>` or :obj:`InputUserFromMessage <pyrogram.api.types.InputUserFromMessage>`
        fwd_limit: ``int`` ``32-bit``

    Returns:
        Either :obj:`UpdatesTooLong <pyrogram.api.types.UpdatesTooLong>`, :obj:`UpdateShortMessage <pyrogram.api.types.UpdateShortMessage>`, :obj:`UpdateShortChatMessage <pyrogram.api.types.UpdateShortChatMessage>`, :obj:`UpdateShort <pyrogram.api.types.UpdateShort>`, :obj:`UpdatesCombined <pyrogram.api.types.UpdatesCombined>`, :obj:`Update <pyrogram.api.types.Update>` or :obj:`UpdateShortSentMessage <pyrogram.api.types.UpdateShortSentMessage>`
    """

    __slots__ = ["chat_id", "user_id", "fwd_limit"]

    ID = 0xf9a0aa09
    QUALNAME = "functions.messages.AddChatUser"

    def __init__(self, *, chat_id: int, user_id, fwd_limit: int):
        self.chat_id = chat_id  # int
        self.user_id = user_id  # InputUser
        self.fwd_limit = fwd_limit  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "AddChatUser":
        # No flags
        
        chat_id = Int.read(b)
        
        user_id = TLObject.read(b)
        
        fwd_limit = Int.read(b)
        
        return AddChatUser(chat_id=chat_id, user_id=user_id, fwd_limit=fwd_limit)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.chat_id))
        
        b.write(self.user_id.write())
        
        b.write(Int(self.fwd_limit))
        
        return b.getvalue()
