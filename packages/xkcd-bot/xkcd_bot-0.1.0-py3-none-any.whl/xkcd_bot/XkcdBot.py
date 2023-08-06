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

import json
import requests
from typing import List, Dict, Any, Optional
from bokkichat.entities.message.MediaType import MediaType
from bokkichat.entities.message.MediaMessage import MediaMessage
from kudubot.Bot import Bot
from kudubot.db.Address import Address
from kudubot.parsing.CommandParser import CommandParser
from sqlalchemy import desc
from sqlalchemy.orm import Session
from xkcd_bot import version
from xkcd_bot.XkcdCommandParser import XkcdCommandParser
from xkcd_bot.db.Comic import Comic
from xkcd_bot.db.Subscription import Subscription


class XkcdBot(Bot):
    """
    The Xkcd Bot class that defines the bot's functionality
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The name of the bot
        """
        return "xkcd-bot"

    @classmethod
    def version(cls) -> str:
        """
        :return: The current version of the bot
        """
        return version

    @classmethod
    def parsers(cls) -> List[CommandParser]:
        """
        :return: A list of parser the bot supports for commands
        """
        return [XkcdCommandParser()]

    def on_subscribe(
            self,
            address: Address,
            _: Dict[str, Any],
            db_session: Session
    ):
        """
        Creates a new subscription for the user
        :param address: The user's address
        :param _: The arguments for the command
        :param db_session: The database session to use
        :return: None
        """
        existing = db_session.query(Subscription)\
            .filter_by(address=address).first()
        if existing is not None:
            self.send_txt(address, "You are already subscribed")
        else:
            subscription = Subscription(
                address=address,
                last_comic_id=self.__get_latest_comic_id(db_session)
            )
            db_session.add(subscription)
            db_session.commit()
            self.logger.info("{} subscribed".format(address.address))
            self.send_txt(address, "Subscription successful")

    def on_unsubscribe(
            self,
            address: Address,
            _: Dict[str, Any],
            db_session: Session
    ):
        """
        Unsubscribes a user
        :param address: The user's address
        :param _: The arguments for the command
        :param db_session: The database session to use
        :return: None
        """
        subscription = db_session.query(Subscription) \
            .filter_by(address=address).first()
        if subscription is not None:
            db_session.delete(subscription)
            db_session.commit()
            self.logger.info("{} unsubscribed".format(address.address))
        self.send_txt(address, "Successfully unregistered")

    def on_new(
            self,
            address: Address,
            _: Dict[str, Any],
            db_session: Session
    ):
        """
        Sends the newest XKCD comic
        :param address: The user's address
        :param _: The arguments for the command
        :param db_session: The database session to use
        :return: None
        """
        latest_id = self.__get_latest_comic_id(db_session)
        self.on_show(address, {"id": latest_id}, db_session)

    def on_show(
            self,
            address: Address,
            args: Dict[str, Any],
            db_session: Session
    ):
        """
        Sends a specific XKCD comic
        :param address: The user's address
        :param args: The arguments for the command
        :param db_session: The database session to use
        :return: None
        """
        comic_id = args["id"]
        comic = self.__get_comic(comic_id, db_session)

        if comic is not None:
            self.__send_comic(comic, address)
        else:
            self.send_txt(address, "This comic does not exist")

    def __get_comic(self, comic_id: int, db_session: Session) \
            -> Optional[Comic]:
        """
        Retrieves a specific XKCD comic from the database or the xkcd website
        :param comic_id: The comic's ID
        :param db_session: The database session to use
        :return: The comic, or None if the comic does not exist
        """
        comic = db_session.query(Comic).filter_by(id=comic_id).first()
        if comic is None:
            self.logger.debug("Comic {} not in database, fetching"
                              .format(comic_id))
            url = "https://xkcd.com/{}/info.0.json".format(comic_id)
            resp = requests.get(url)
            if resp.status_code >= 300:
                comic = None
                self.logger.debug("Comic {} does not exist".format(comic_id))
            else:
                data = json.loads(resp.text)
                comic = Comic(
                    id=data["num"],
                    title=data["title"],
                    alt_text=data["alt"],
                    image_url=data["img"],
                    image_data=requests.get(data["img"]).content
                )
                self.logger.debug("Successfully downloaded comic {}"
                                  .format(comic_id))
                db_session.add(comic)
                db_session.commit()
        return comic

    def __get_latest_comic_id(
            self,
            db_session: Session,
            refresh: bool = False
    ) -> int:
        """
        Retrieves the latest comic ID
        :param db_session: The database session to use
        :param refresh: Whether or not to retrieve the most up-to-date info
        :return: The ID of the newest comic
        """
        if not refresh:
            self.logger.debug("Loading newest comic ID")
            latest = db_session.query(Comic).order_by(desc(Comic.id)).first()
            if latest is None:
                return self.__get_latest_comic_id(db_session, True)
            else:
                return latest.id
        else:
            resp = requests.get("https://xkcd.com/info.0.json").text
            data = json.loads(resp)
            return data["num"]

    def __send_comic(self, comic: Comic, address: Address):
        """
        Sends a comic to a user
        :param comic: The comic to send
        :param address: The address of the user
        :return: None
        """
        self.logger.info("Sending comic {} to {}"
                         .format(comic.id, address.address))
        self.send_txt(address, comic.title)
        message = MediaMessage(
            self.connection.address,
            address, MediaType.IMAGE,
            comic.image_data,
            comic.alt_text
        )
        self.connection.send(message)

    def bg_iteration(self, _: int, db_session: Session):
        """
        Periodically checks for new notifications and sends them out
        :param _: The iteration count
        :param db_session: The database session to use
        :return: None
        """
        self.logger.info("Looking for due subscriptions")

        latest_id = self.__get_latest_comic_id(db_session, True)
        comic = self.__get_comic(latest_id, db_session)
        if comic is None:
            self.logger.error("Latest comic did not load")
            return

        for subscription in db_session.query(Subscription).all():
            if subscription.last_comic_id < latest_id:
                self.logger.info("Subscription for {} is due"
                                 .format(subscription.address.address))
                self.__send_comic(comic, subscription.address)
                subscription.last_comic = comic

        db_session.commit()
