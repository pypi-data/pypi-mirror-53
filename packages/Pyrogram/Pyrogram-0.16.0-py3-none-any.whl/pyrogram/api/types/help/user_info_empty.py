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


class UserInfoEmpty(TLObject):
    """Attributes:
        LAYER: ``105``

    Attributes:
        ID: ``0xf3ae2eed``

    No parameters required.

    See Also:
        This object can be returned by :obj:`help.GetUserInfo <pyrogram.api.functions.help.GetUserInfo>` and :obj:`help.EditUserInfo <pyrogram.api.functions.help.EditUserInfo>`.
    """

    __slots__ = []

    ID = 0xf3ae2eed
    QUALNAME = "types.help.UserInfoEmpty"

    def __init__(self, ):
        pass

    @staticmethod
    def read(b: BytesIO, *args) -> "UserInfoEmpty":
        # No flags
        
        return UserInfoEmpty()

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
