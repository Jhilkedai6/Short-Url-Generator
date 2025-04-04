from sqlalchemy import String, Integer, Column, Date
from database import Base


class Url(Base):
    __tablename__ = "url_table"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String)
    short_url = Column(String, unique=True)
    created_date = Column(Date)
    updated_date = Column(Date)
    access_count = Column(Integer)


class ShortCode(Base):
    __tablename__ = "shortcode_table"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String)