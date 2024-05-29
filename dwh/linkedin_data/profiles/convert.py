"""
This module contains functions to convert document data to DWH tables.

"""
import pandas as pd
import datetime


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
        'inferredSalaryMin': document.get('inferred_salary').get('min') if document.get('inferred_salary') else None,
        'inferredSalaryMax': document.get('inferred_salary').get('max') if document.get('inferred_salary') else None,
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


def experience(experience_object: dict, key_person: int, key_duration: int):
    """
    This function converts qualifications to the FACT_PRF_Qualification table.

    :param key_person: The ID of the person entry in the DWH.
    :param experience_object: The experience object to convert.
    :param key_duration: The ID of the duration entry in the DWH.
    """

    # Create and fill the table
    experience_dict = {
        'idPerson': key_person,
        'idDuration': key_duration,
        'type': 'experience',
        'name': experience_object.get('title'),
        'institution': experience_object.get('company'),
        'description': experience_object.get('description')
    }

    # Create and return DataFrame
    return pd.DataFrame([experience_dict])


def education(education_object: dict, key_person: int, key_duration: int):
    """
    This function converts qualifications to the FACT_PRF_Qualification table.

    :param key_person: The ID of the person entry in the DWH.
    :param education_object: The education object to convert.
    :param key_duration: The ID of the duration entry in the DWH.
    """

    degree_name = education_object.get('degree_name', None)
    field_of_study = education_object.get('field_of_study', None)

    # Use match case to determine the value of 'name'
    match (degree_name, field_of_study):
        case (None, None):
            name = None
        case (None, _):
            name = field_of_study
        case (_, None):
            name = degree_name
        case _:
            name = f"{degree_name} in {field_of_study}"

    # Create and fill the table
    experience_dict = {
        'idPerson': key_person,
        'idDuration': key_duration,
        'type': 'education',
        'name': name,
        'institution': education_object.get('school'),
        'description': education_object.get('description')
    }

    # Create and return DataFrame
    return pd.DataFrame([experience_dict])


def volunteer_work(volunteer_object: dict, key_person: int, key_duration: int):
    """
    This function converts qualifications to the FACT_PRF_Qualification table.

    :param key_person: The ID of the person entry in the DWH.
    :param volunteer_object: The volunteer object to convert.
    :param key_duration: The ID of the duration entry in the DWH.
    """

    # Get the cause and description
    cause = volunteer_object.get('cause', None)
    description = volunteer_object.get('description', None)

    # Use match case to determine the description
    match (cause, description):
        case (None, None):
            comb_description = None
        case (None, _):
            comb_description = description
        case (_, None):
            comb_description = cause
        case _:
            comb_description = f"Cause: {cause} | Description:{description}"

    # Create and fill the table
    experience_dict = {
        'idPerson': key_person,
        'idDuration': key_duration,
        'type': 'volunteer',
        'name': volunteer_object.get('title'),
        'institution': volunteer_object.get('company'),
        'description': comb_description
    }

    # Create and return DataFrame
    return pd.DataFrame([experience_dict])


def certification(certification_object: dict, key_person: int, key_duration: int):
    """
    This function converts qualifications to the FACT_PRF_Qualification table.

    :param key_person: The ID of the person entry in the DWH.
    :param certification_object: The certification object to convert.
    :param key_duration: The ID of the duration entry in the DWH.
    """

    # Get the license number and display source
    license_number = certification_object.get('license_number', None)
    display_source = certification_object.get('display_source', None)

    # Use match case to determine the description
    match (license_number, display_source):
        case (None, None):
            comb_description = None
        case (None, _):
            comb_description = display_source
        case (_, None):
            comb_description = license_number
        case _:
            comb_description = f"Cause: {license_number} | Description:{display_source}"

    # Create and fill the table
    experience_dict = {
        'idPerson': key_person,
        'idDuration': key_duration,
        'type': 'certification',
        'name': certification_object.get('name'),
        'institution': certification_object.get('authority'),
        'description': comb_description
    }

    # Create and return DataFrame
    return pd.DataFrame([experience_dict])


def accomplishment_projects(accomplishment_object: dict, key_person: int, key_duration: int):
    """
    This function converts qualifications to the FACT_PRF_Qualification table.

    :param key_person: The ID of the person entry in the DWH.
    :param accomplishment_object: The accomplishment object to convert.
    :param key_duration: The ID of the duration entry in the DWH.
    """

    # Create and fill the table
    experience_dict = {
        'idPerson': key_person,
        'idDuration': key_duration,
        'type': 'project',
        'name': accomplishment_object.get('title'),
        'institution': None,
        'description': accomplishment_object.get('description')
    }

    # Create and return DataFrame
    return pd.DataFrame([experience_dict])
