"""
This module contains functions to convert document data to DWH tables.

"""
import pandas as pd
import datetime


def location(location_object: dict) -> pd.DataFrame:
    """
    This function converts a location to the FACT_LIN_Location table.

    :param location_object: The dictionary to convert.
    """
    country_letters = None
    country_name = None

    if location_object.get('country'):
        strip_country = location_object.get('country').strip()
        if len(strip_country) <= 2:
            country_letters = strip_country
        else:
            country_name = strip_country

    if location_object.get('state'):
        loc_state = location_object.get('state')
    else:
        loc_state = location_object.get('postal_code')

    # Create and fill the table
    location_dict = {
        'countryLetters': country_letters,
        'countryName': country_name,
        'state': loc_state,
        'city': location_object.get('city')
    }

    # Create and return DataFrame
    return pd.DataFrame([location_dict])


def company(document: dict, dimension_key_hq: int, dimension_key_origin: int) -> pd.DataFrame:
    """
    This function converts a company to the FACT_CMP_Company table.

    :param document: The document to convert.
    :param dimension_key_hq: The ID of the hq location dimension entry.
    :param dimension_key_origin: The ID of the origin in the DWH.
    """
    # Get the size attributes
    size_a = None
    size_b = None
    if document.get('company_size'):
        if document.get('company_size')[0]:
            size_a = document.get('company_size')[0]
        if document.get('company_size')[1]:
            size_b = document.get('company_size')[1]

    # Create and fill the table
    company_dict = {
        'idHqLocation': dimension_key_hq,
        'industry': document.get('industry'),
        'type': document.get('company_type'),
        'founded': document.get('founded_year'),
        'name': document.get('name'),
        'tagline': document.get('tagline'),
        'sizeA': size_a,
        'sizeB': size_b,
        'sizeLinkedIn': document.get('company_size_on_linkedin'),
        'followers': document.get('follower_count'),
        'website': 1 if document.get('website') else 0,
        'profilePicture': 1 if document.get('profile_pic_url') else 0,
        'backgroundPicture': 1 if document.get('background_cover_image_url') else 0,
        'description': document.get('description'),
        'mongoCollectionId': document.get('_id'),
        'idOrigin': dimension_key_origin
    }

    # Create and return DataFrame
    return pd.DataFrame([company_dict])


def convert_date(date_object: dict) -> datetime.date | None:
    """
        This function converts a date dictionary from MongoDB to a Python datetime.date object.
        This date can be inserted into a MySQL DATE column as it inherently matches the required format.

        :param date_object: The date dictionary to convert.
        :return: A date object or None if the date is not complete.
    """
    if date_object and all(k in date_object for k in ['year', 'month', 'day']):
        return datetime.date(year=date_object['year'], month=date_object['month'], day=date_object['day'])
    else:
        return None
