"""
Module containing SQLAlchemy models.
"""
from sqlalchemy import Column, Integer, String
from .database import Base


class Ads(Base): # pylint: disable=R0903
    """
    The database model for the table  with all the listings.
    """
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, unique=False, index=True)
    url = Column(String, unique=False, index=True)
    price = Column(Integer, unique=False, index=True)
    home_type = Column(String, unique=False, index=True)
    home_size = Column(Integer, unique=False, index=True)
    location = Column(String, unique=False, index=True)
    image = Column(String, unique=False, index=True)
    scraping_date = Column(String, unique=False, index=True)


class NewAds(Base): # pylint: disable=R0903
    """
    Table containing only the new listings that have been collected.
    """
    __tablename__ = "new_ads"
    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, unique=False, index=True)
    url = Column(String, unique=False, index=True)
    price = Column(Integer, unique=False, index=True)
    home_type = Column(String, unique=False, index=True)
    home_size = Column(Integer, unique=False, index=True)
    location = Column(String, unique=False, index=True)
    image = Column(String, unique=False, index=True)
    scraping_date = Column(String, unique=False, index=True)
