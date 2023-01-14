"""
Modulel holding utility helper functions.
"""
import os
from . import constants

__all__ = ["create_db_folder"]


def create_db_folder():
    """
    Create the data folder (if not created) where the database will be created.
    """
    if not os.path.exists(constants.DATA_DIR):
        os.mkdir(constants.DATA_DIR)
