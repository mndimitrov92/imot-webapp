"""
Module containing the Pydantic models.
"""
from pydantic import BaseModel


class Ads(BaseModel):
    """
    Pydantic model for the ads table.
    """

    id: int
    title: str
    source_name: str
    url: str
    price: int
    home_type: str
    home_size: int
    location: str
    # location_orig: str
    image: str
    scraping_date: str
    taken_from: str
    # Adding this configuration will tell the model to read the data
    # even if it's not a dict but a model so
    # data could be retrieved in both ways:
    # data['item']
    # data.item

    class Config:
        orm_mode = True


class NewAds(BaseModel):
    """
    Pydantic model for the new ads table.
    """


class Summary(BaseModel):
    """
    Pydantic model for the summary table.
    """
    id: int
    addressbg: int
    arcoreal: int
    avista: int
    bulgarianproperties: int
    era: int
    galardo: int
    home2u: int
    imotbg: int
    luximmo: int
    mirelabg: int
    novdom1: int
    place2live: int
    primoplus: int
    superimoti: int
    ues: int
    yavlena: int
    yourhome: int
