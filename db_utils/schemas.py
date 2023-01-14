"""
Module containing the Pydantic models.
"""
import pydantic


class Ads(pydantic.BaseModel): # pylint-disable=E1101
    """
    Pydantic model for the ads table.
    """
    id: int
    source_name: str
    url: str
    price: int
    home_type: str
    home_size: int
    location: str
    image: str
    scraping_date: str
    # Adding this configuration will tell the model to read the data
    # even if it's not a dict but a model so
    # data could be retrieved in both ways:
    # data['item']
    # data.item

    class Config:
        """
        Helper configuration class for easier property retrieval.
        """
        orm_mode = True


class NewAds(Ads):
    """
    Pydantic model for the new ads table.
    """
