"""
Module for the collection of all needed constants.
"""
import os
import enum


__all__ = ["STATIC_DIR", "AdSource", "AdLocation"]



STATIC_DIR = os.path.join(os.getcwd(), 'static')

class AdSource(enum.Enum):
    """
    Enumeration class that provides the allowed source names.
    The API will use them for the input validations.
    """
    IMOTBG = "imotbg"
    YAVLENA = "yavlena"
    BULGARIANPROPERTIES = "buildagianproperties"
    ERA = "era"
    # TODO FIll in the rest of the sources


class AdLocation(enum.Enum):
    """
    Enumeration class that provides the allowed os names.
    The API will use them for the input validations.
    """
    SUHATA_REKA = "Suhata reka"
    DURVENICA = "Durvenica"
    MLADOST2 = "Mladost 2"
    # TODO: Add all popssible locations
