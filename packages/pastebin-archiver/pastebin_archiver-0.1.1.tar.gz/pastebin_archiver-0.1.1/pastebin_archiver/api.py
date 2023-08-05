import logging
from datetime import datetime
from typing import List
from json.decoder import JSONDecodeError

import requests
from requests.exceptions import HTTPError

from .database import Database
from .event_queue import EventQueue
from .exceptions import ExpiredError
from .models import Content, Metadata


class API:
    """Class for fetching data from the Pastebin API and storing it in the database"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.database = Database()
        self.event_queue = EventQueue()

    def fetch_content(self, record: Metadata) -> Content:
        """
        Fetch the content (body) of a post from the Pastebin API.

        :param record: the Metadata object for the post to fetch
        :returns: a copy of the Content object that was stored in the database
        :raises ExpiredError: the requested record is expired
        """

        now = datetime.utcnow()

        if record.expire < now:
            self.logger.warning(f"Requested record is expired: {record}")
            raise ExpiredError(
                f"The requested record is expired (expires {record.expire}, currently {now})"
            )

        try:
            r = requests.get(record.scrape_url)
            r.raise_for_status()
            body = r.text
        except HTTPError as e:
            self.logger.error(f"Content request recieved error response: {e}")
            self.event_queue.enqueue(self.fetch_content, {"record": record})

        session = self.database.Session()
        content = Content(id=record.id, body=body)
        session.add(content)
        session.commit()
        return content

    def fetch_metadata(self) -> List[Metadata]:
        """
        Fetch the metadata of all new posts from the Pastebin API,
        store them in the database, and queue events to fetch their content.

        :returns: a list of the Metadata objects that were stored and queued
        """
        url = "https://scrape.pastebin.com/api_scraping.php?limit=100"

        try:
            r = requests.get(url)
            r.raise_for_status()
            body = r.json()
            self.logger.info(f"Fetched metadata for {len(body)} records")
        except HTTPError as e:
            self.logger.error(f"Metadata request recieved error response: {e}")
            return list()
        except JSONDecodeError:
            self.logger.error(
                f"No posts were found - perhaps your IP address is not whitelisted?"
            )
            self.logger.debug(
                f"Failed to parse metadata API response as JSON. Response body: {r.text}"
            )
            return list()

        records = [Metadata(**x) for x in body]

        session = self.database.Session()
        latest = session.query(Metadata).order_by(Metadata.date.desc()).first()
        self.logger.debug(f"Latest record queried: {latest}")
        if latest is None:
            self.logger.info("No existing metadata found, all queried posts are new.")
        else:
            if (latest.key, latest.date) not in [
                (x.get("key"), datetime.utcfromtimestamp(int(x.get("date"))))
                for x in body
            ]:
                self.logger.warning(
                    " ".join(
                        [
                            f"Posts may have been missed"
                            f"(oldest fetched record created {body[-1]['date']},",
                            f"latest saved record created {latest.date})",
                        ]
                    )
                )

            records = [x for x in records if x.date > latest.date]
            self.logger.info(f"Identified {len(records)} new metadata records")

        if len(records) == 0:
            return list()

        session.add_all(records)
        session.commit()

        records.sort(key=lambda x: x.expire)
        for r in records:
            self.event_queue.enqueue(self.fetch_content, {"record": r})

        return records
