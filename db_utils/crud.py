"""
Module for basic CRUD operations.
"""
from sqlalchemy.orm import Session
from . import models


def get_filtered_ads(db_session: Session, #pylint: disable=R0913
                     source_name: str = None,
                     price: int = None,
                     location: str = None,
                     home_size: int = None,
                     home_type: str = None,
                     limit: int = 10000,
                     only_new_ads: bool = False):
    """
    Retrieve all ads based on the filters passed.
    Params:
    db: the database session
    source_name(Optional): The name of which the ad list will be filtered by:
              (these are the spider names)
    price(Optional): The price less than which the ad list will be filtered by:

    location(Optional): The location of which the ad list will be filtered by
    home_size(Optional): The home_size more than which the ad list will be filtered by
    home_type(Optional): The home type of which the ad list will be filtered by
    limit(Optional): The amount of entries to be shown
    only_new_ads: Flag to indicate whether all ads will be displayed or only the new ones
    """
    model_ads = models.NewAds if only_new_ads else models.Ads

    output = db_session.query(model_ads)
    if source_name is not None:
        output = output.filter(model_ads.source_name == source_name.value)
    if location is not None:
        output = output.filter(model_ads.location == location.value)
    if home_type is not None:
        output = output.filter(model_ads.home_type == home_type.value)
    if price is not None:
        output = output.filter(
            model_ads.price < price)
    if home_size is not None:
        output = output.filter(
            model_ads.home_size > home_size)
    return output.limit(limit).all()


def get_ordered_ads(db_session: Session, limit: int = 10000, only_new_ads: bool = False):
    """
    Retrieve all ads ordered by price - location - home-size - source_name - home-type.
    Params:
    db_session: the database session
    limit(Optional): The amount of entries to be shown
    only_new_ads: Flag to indicate whether all ads will be displayed or only the new ones
    """
    model_ads = models.NewAds if only_new_ads else models.Ads
    order_precedence = ("price", "location", "home_size",
                        "source_name", "home_type")
    output = db_session.query(model_ads)
    return output.order_by(*order_precedence).limit(limit).all()
