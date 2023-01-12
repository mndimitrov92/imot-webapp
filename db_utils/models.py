"""
Module containing SQLAlchemy models.
"""
from sqlalchemy import Column, Integer, String
from .database import Base


class Ads(Base):
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


class NewAds(Base):
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


class Summary(Base):
    """
    Summary table containing the amount of listings found for each source.
    """
    __tablename__ = "summary"

    id = Column(Integer, primary_key=True, index=True)
    addressbg = Column(Integer, unique=False, index=True)
    arcoreal = Column(Integer, unique=False, index=True)
    avista = Column(Integer, unique=False, index=True)
    bulgarianproperties = Column(Integer, unique=False, index=True)
    era = Column(Integer, unique=False, index=True)
    galardo = Column(Integer, unique=False, index=True)
    home2u = Column(Integer, unique=False, index=True)
    imotbg = Column(Integer, unique=False, index=True)
    luximmo = Column(Integer, unique=False, index=True)
    mirelabg = Column(Integer, unique=False, index=True)
    novdom1 = Column(Integer, unique=False, index=True)
    place2live = Column(Integer, unique=False, index=True)
    primoplus = Column(Integer, unique=False, index=True)
    superimoti = Column(Integer, unique=False, index=True)
    ues = Column(Integer, unique=False, index=True)
    yavlena = Column(Integer, unique=False, index=True)
    yourhome = Column(Integer, unique=False, index=True)
    bezkomisiona = Column(Integer, unique=False, index=True)
