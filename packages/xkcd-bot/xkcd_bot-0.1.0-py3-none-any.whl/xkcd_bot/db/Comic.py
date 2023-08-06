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
from sqlalchemy import Column, Integer, String, Binary


class Comic(Base):
    """
    Models an XKCD comic
    """

    __tablename__ = "comics"
    """
    The name of the database table
    """

    id = Column(Integer, primary_key=True)
    """
    The ID of the comic (same as on the website itself)
    """

    image_url = Column(String(255), nullable=False)
    """
    The URL of the image for this comic
    """

    title = Column(String(255), nullable=False)
    """
    The comic's title
    """

    alt_text = Column(String(255), nullable=False)
    """
    The comic's alt text
    """

    image_data = Column(Binary, nullable=False)
    """
    The image's data
    """
