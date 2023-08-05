from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

Base = declarative_base()


class Metadata(Base):
    __tablename__ = "metadata"

    id = Column(Integer, primary_key=True)
    key = Column(String(8))
    date = Column(DateTime)
    size = Column(Integer)
    expire = Column(DateTime)
    title = Column(String(60))
    syntax = Column(String(16))
    user = Column(String(20))
    scrape_url = Column(String(64))
    full_url = Column(String(32))

    def __repr__(self):
        return "".join(
            [
                f"<Metadata(",
                f"key='{self.key}', ",
                f"size='{self.size}', ",
                f"date='{self.date}', ",
                f"expire='{self.expire}', ",
                f"title='{self.title}', ",
                f")>",
            ]
        )

    @validates("date")
    def validate_date(self, key, date):
        if type(date) is str:
            date = datetime.utcfromtimestamp(int(date))
        elif type(date) is int:
            date = datetime.utcfromtimestamp(date)
        assert type(date) is datetime
        return date

    @validates("expire")
    def validate_expire(self, key, expire):
        if type(expire) is str:
            if expire == "0":
                expire = datetime.max
            else:
                expire = datetime.utcfromtimestamp(int(expire))
        elif type(expire) is int:
            if expire == 0:
                expire = datetime.max
            else:
                expire = datetime.utcfromtimestamp(expire)
        assert type(expire) is datetime
        return expire


class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, ForeignKey("metadata.id"), primary_key=True)
    body = Column(Text)

    def __repr__(self):
        return f"<Content(id={self.id})>"
