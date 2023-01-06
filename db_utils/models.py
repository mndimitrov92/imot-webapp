"""
Module containing SQLAlchemy models.
"""
from sqlalchemy import Column, Integer, String
from .database import Base


class Ads(Base):
    """
    The test table ads database model.
    """
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=False, index=True)
    source_name = Column(String, unique=False, index=True)
    url = Column(String, unique=False, index=True)
    price = Column(Integer, unique=False, index=True)
    home_type = Column(String, unique=False, index=True)
    home_size = Column(Integer, unique=False, index=True)
    location = Column(String, unique=False, index=True)
    image = Column(String, unique=False, index=True)
    scraping_date = Column(String, unique=False, index=True)
    taken_from = Column(String, unique=False, index=True)

#TODO: Fill in with the models for all the tables
