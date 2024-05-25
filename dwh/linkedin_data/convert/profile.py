"""
This module contains functions to convert document data to DWH tables.

"""
import pandas as pd


def person(document: dict, dimension_key_location: int, dimension_key_origin: int) -> pd.DataFrame:
    """
    This function converts a profile to the FACT_PRF_Person table.

    :param document: The document to convert.
    :param dimension_key_location: The ID of the location dimension.
    :param dimension_key_origin: The ID of the origin in the DWH.
    """

    # Create and fill the table
    person_dict = {
        'idLocation': dimension_key_location,
        'name': document.get('full_name'),
        'occupation': document.get('occupation'),
        'headline': document.get('headline'),
        'summary': document.get('summary'),
        'connections': document.get('connections'),
        'inferredSalaryMin': document.get('inferred_salary', {}).get('min'),
        'inferredSalaryMax': document.get('inferred_salary', {}).get('max'),
        'gender': document.get('gender'),
        'industry': document.get('industry'),
        'profilePicture': 1 if document.get('profile_pic_url') else 0,
        'backgroundPicture': 1 if document.get('background_cover_image_url') else 0,
        'mongoCollectionId': document.get('_id'),
        'idOrigin': dimension_key_origin
    }

    # Create and return DataFrame
    return pd.DataFrame([person_dict])


def location(document) -> pd.DataFrame:
    """
    This function converts a location to the FACT_LIN_Location table.

    :param document: The document to convert.
    """

    # Create and fill the table
    location_dict = {
        'countryLetters': document.get('country'),
        'countryName': document.get('country_full_name'),
        'state': document.get('state'),
        'city': document.get('city')
    }

    # Create and return DataFrame
    return pd.DataFrame([location_dict])
