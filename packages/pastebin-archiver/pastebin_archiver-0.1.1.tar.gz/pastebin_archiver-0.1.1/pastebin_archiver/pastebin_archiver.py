import logging
from datetime import datetime
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .api import API
from .database import Database
from .event_queue import EventQueue
from .models import Content, Metadata


class PastebinArchiver:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.database = Database()
        self.event_queue = EventQueue()
        self.scheduler = BackgroundScheduler()
        self.api = API()

    def main(self):
        """Main entry-point for the application"""
        self.logger.info(f"Starting at {datetime.utcnow()}")
        records = self.query_missing_content()
        for r in records:
            self.event_queue.enqueue(self.api.fetch_content, {"record": r})

        self.scheduler.start()
        self.scheduler.add_job(
            func=self.event_queue.enqueue,
            trigger=IntervalTrigger(minutes=1),
            kwargs={"function": self.api.fetch_metadata, "priority": True},
            misfire_grace_time=10,
            coalesce=True,
        )

        self.event_queue.enqueue(self.api.fetch_metadata)

        self.logger.debug("Entering event loop")
        self.event_loop()

    def event_loop(self):
        """Execute events as quickly as possible, idling if queue is empty. This function does not return."""
        while True:
            event = self.event_queue.next()
            if event:
                self.logger.debug(f"Running event {event}")
                event.run()
            else:
                self.logger.debug(
                    f"Event loop is empty, polling new events every 5 seconds."
                )
                sleep(5)

    def query_missing_content(self):
        """
        Queries the database for non-expired metadata that is missing content.

        :returns: a list of Metadata objects which need content
        """
        session = self.database.Session()
        records = (
            session.query(Metadata)
            .outerjoin(Content)
            .filter(Content.id.is_(None))
            .filter(Metadata.expire > datetime.utcnow())
            .order_by(Metadata.expire)
            .all()
        )
        self.logger.info(f"Identified {len(records)} unexpired records missing content")
        return records
