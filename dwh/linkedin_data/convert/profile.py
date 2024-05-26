"""
This module contains functions to convert document data to DWH tables.

"""
import pandas as pd
import datetime


def _convert_date(date) -> datetime.date | None:
    """
        This function converts a date dictionary from MongoDB to a Python datetime.date object.
        This date can be inserted into a MySQL DATE column as it inherently matches the required format.
    
        :param date: The date dictionary to convert.
        :return: A date object or None if the date is not complete.
    """
    if date and all(k in date for k in ['year', 'month', 'day']):
        return datetime.date(year=date['year'], month=date['month'], day=date['day'])
    else:
        return None


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


def location(document: dict) -> pd.DataFrame:
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


def experience(experience_object: dict, key_person: int, key_duration: int = None, key_institution: int = None):
    """
    This function converts qualifications to the FACT_PRF_Qualification table.

    :param key_person: The ID of the person entry in the DWH.
    :param experience_object: The experience object to convert.
    :param key_duration: The ID of the duration entry in the DWH.
    :param key_institution: The ID of the institution entry in the DWH.
    """

    # Create and fill the table
    experience_dict = {
        'idPerson': key_person,
        'idDuration': key_duration,
        'idInstitution': key_institution,
        'type': 'experience',
        'name': experience_object.get('title'),
        'description': experience_object.get('description')
    }

    # Create and fill the duration dimension table
    duration_dict = {
        'startDate': _convert_date(experience_object.get('starts_at')),
        'endDate': _convert_date(experience_object.get('ends_at'))
    }

    # Create and fill the institution dimension table
    institution_dict = {
        'name': experience_object.get('company'),
        'location': experience_object.get('location')
    }

    # Create and return DataFrames
    return pd.DataFrame([experience_dict]), pd.DataFrame([duration_dict]), pd.DataFrame([institution_dict])
