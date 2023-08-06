"""LICENSE
Copyright 2019 Hermann Krumrey <hermann@krumreyh.com>

This file is part of xkcd-bot.

xkcd-bot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

xkcd-bot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with xkcd-bot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

from kudubot.db import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Subscription(Base):
    """
    Models a subscription for new XKCD comics
    """

    __tablename__ = "subscriptions"
    """
    The name of the database table
    """

    id = Column(Integer, primary_key=True, autoincrement=True)
    """
    The ID of the subscription
    """

    address_id = Column(Integer, ForeignKey("addressbook.id"))
    """
    The ID of the associated address
    """

    address = relationship("Address")
    """
    The associated address
    """

    last_comic_id = Column(Integer, ForeignKey("comics.id"))
    """
    The ID of the last subscription comic to be sent to the user
    """

    last_comic = relationship("Comic")
    """
    The last subscription comic to be sent to the user
    """
