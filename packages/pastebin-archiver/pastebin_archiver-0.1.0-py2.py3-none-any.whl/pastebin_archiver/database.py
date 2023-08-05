import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base
from .config import Config


class Database:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug(
            f"Connecting to the database using string: {Config.db_connection_string}"
        )
        self.engine = create_engine(Config.db_connection_string, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
