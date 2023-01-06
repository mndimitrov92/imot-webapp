"""
Module for basic CRUD operations.
"""
from sqlalchemy.orm import Session
from . import models


def get_filtered_ads(db: Session,
                     source_name: str = None,
                     price: str = None,
                     location: int = None,
                     limit: int = 100):
    """
    Retrive all ads based on the filters passed.
    Params:
    db: the database session
    source_name(Optional): The name of which the ad list will be filtered by:
              (these are the spider names)
    price(Optional): The price less than which the ad list will be filtered by:

    location(Optional): The location of which the ad list will be filtered by
    limit(Optional): The amount of entries to be shown
    """
    output = db.query(models.Ads)
    if source_name is not None:
        output = output.filter(models.Ads.source_name == source_name.value)
    if location is not None:
        output = output.filter(models.Ads.location == location.value)
    if price is not None:
        output = output.filter(
            models.Ads.price < price)
    return output.limit(limit).all()


def get_ordered_ads(db: Session, limit: int = 100):
    """
    Retrive all ads ordered by price - location - source_name.
    Params:
    db: the database session
    limit(Optional): The amount of entries to be shown
    """
    order_precedence = ("price", "location", "source_name")
    output = db.query(models.Ads)
    return output.order_by(*order_precedence).limit(limit).all()
