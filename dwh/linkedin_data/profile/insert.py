"""
This module contains functions to process the linkedin documents data.

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


def experiences(document: dict, key_person: int):
    """
    This function inserts all experiences into the FACT_PRF_Qualification table.

    :param document: The experience object to convert.
    :param key_person: The ID of the person entry in the DWH.
    """

    for exp in document.get('experiences', []):
        experience, duration, institution = _process_experience(exp, key_person)
        yield experience, duration, institution
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
