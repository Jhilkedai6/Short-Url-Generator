from sqlalchemy import String, Integer, Column, Date, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    acc_created = Column(Date)
    role = Column(String)

    url = relationship("Url", back_populates="user", cascade="all, delete-orphan")
    short_code = relationship("ShortCode", back_populates="user", cascade="all, delete-orphan")


class Url(Base):
    __tablename__ = "url_table"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String)
    short_url = Column(String, unique=True)
    created_date = Column(Date)
    updated_date = Column(Date)
    access_count = Column(Integer, default=0)
    expire_time = Column(DateTime)
    status = Column(String)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    user = relationship("User", back_populates="url")



class ShortCode(Base):
    __tablename__ = "shortcode_table"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String)
    expire = Column(DateTime)
    user_id = Column(Integer, ForeignKey("user_table.id"))

    user = relationship("User", back_populates="short_code")



class Logs(Base):
    __tablename__ = "log_table"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    username = Column(String)
    activity = Column(String)
    time = Column(DateTime)



