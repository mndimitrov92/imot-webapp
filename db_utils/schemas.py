"""
Module containing the Pydantic models.
"""
from pydantic import BaseModel


class Ads(BaseModel):
    """
    Pydantic model for the ads test table 
    """

    id : int
    title: str
    source_name: str
    url: str
    price: int
    home_type: str
    home_size: int
    location: str
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

# TODO: Populate with the schemas for the each table
