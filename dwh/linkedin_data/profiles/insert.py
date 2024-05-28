"""
This module holds the functions used to import the individual attributes into the DWH.
"""
import pandas as pd
import sqlalchemy  # Requires pymysql
from datetime import datetime
# Import conversion functions
from dwh.linkedin_data.profiles import convert as conv


def location(document: dict, dwh_engine) -> int:
    """
    This function inserts a location into the DWH and returns its ID.

    DWH table: DIM_LIN_Location

    :param document: The document to convert.
    :param dwh_engine: The DWH engine to use.
    """
    # Prepare location data
    location_df = conv.location(document)

    # Check if a matching record exists
    query = """
        SELECT id
        FROM DIM_LIN_Location
        WHERE countryLetters = %(countryLetters)s 
        AND countryName = %(countryName)s
        AND city = %(city)s
        AND state = %(state)s
    """
    result = pd.read_sql_query(query, dwh_engine, params=location_df.iloc[0].to_dict())

    if not result.empty:
        # If matching record found, use existing id
        location_id = result.iloc[0]['id']
    else:
        # If no matching record found, insert a new record and use its id
        location_df.to_sql('DIM_LIN_Location', dwh_engine, if_exists='append', index=False)
        location_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]
    
    # Return location id
    return location_id


def person(document: dict, location_id: int, origin_id: int, dwh_engine) -> int:
    """
    This function inserts a person into the DWH and returns its ID.

    DWH table: FACT_PRF_Person

    :param document: The document to convert.
    :param location_id: The ID of the location dimension.
    :param origin_id: The ID of the DIM_Origin table from the dwh.
    :param dwh_engine: The DWH engine to use.
    """
    # Prepare person data
    person_df = conv.person(document, location_id, origin_id)

    # Insert person data
    person_df.to_sql('FACT_PRF_Person', dwh_engine, if_exists='append', index=False)
    person_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]

    # Return person id
    return person_id


def recommendations(document: dict, person_id: int, dwh_engine):
    """
    This function inserts recommendations into the DWH.

    DWH table: FACT_PRF_Recommendation

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('recommendations'):
        recommendations = document.get('recommendations', [])
        data = []

        # Populate list with data
        for rec in recommendations:
            data.append({
                'idPerson': person_id,
                'recommendationText': rec
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Recommendation', dwh_engine, if_exists='append', index=False)


def people_also_viewed(document: dict, person_id: int, dwh_engine):
    """
    This function inserts people also viewed into the DWH.

    DWH table: FACT_PRF_Related

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('people_also_viewed'):
        df_to_add = document.get('people_also_viewed', [])
        data = []

        # Populate list with data
        for ppl in df_to_add:
            data.append({
                'idPerson': person_id,
                'type': 'viewed',
                'name': ppl.get('name'),
                'location': ppl.get('location'),
                'summary': ppl.get('summary')
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Related', dwh_engine, if_exists='append', index=False)
    

def similarly_named_profiles(document: dict, person_id: int, dwh_engine):
    """
    This function inserts similarly named profiles into the DWH.

    DWH table: FACT_PRF_Related

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('similarly_named_profiles'):
        df_to_add = document.get('similarly_named_profiles', [])
        data = []

        # Populate list with data
        for ppl in df_to_add:
            data.append({
                'idPerson': person_id,
                'type': 'similar',
                'name': ppl.get('name'),
                'location': ppl.get('location'),
                'summary': ppl.get('summary')
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Related', dwh_engine, if_exists='append', index=False)


def languages(document: dict, person_id: int, dwh_engine):
    """
    This function inserts languages into the DWH.

    DWH tables: DIM_PRF_Language, REL_PRF_Person_Language

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('languages') and len(document.get('languages')) > 0:
        for lang in document.get('languages'):
            # Check if a matching record exists
            query = """
                SELECT id
                FROM DIM_PRF_Language
                WHERE language = %(language)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'language': lang})

            if not result.empty:
                # If matching record found, use existing id
                lang_id = result.iloc[0]['id']
            else:
                # If no matching record found, insert a new record and use its id
                pd.DataFrame({
                    'language': [lang]
                }).to_sql('DIM_PRF_Language', dwh_engine, if_exists='append', index=False)
                lang_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]

            # Check if a relationship record already exists
            query = """
                SELECT *
                FROM REL_PRF_Person_Language
                WHERE idPerson = %(idPerson)s
                AND idLanguage = %(idLanguage)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'idPerson': person_id, 'idLanguage': lang_id})

            # Insert if relationship record does not exist
            if result.empty:
                pd.DataFrame([{
                    'idPerson': person_id,
                    'idLanguage': lang_id
                }]).to_sql('REL_PRF_Person_Language', dwh_engine, if_exists='append', index=False)


def skills(document: dict, person_id: int, dwh_engine):
    """
    This function inserts skills into the DWH.

    DWH tables: DIM_PRF_Trait, REL_PRF_Person_Trait

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('skills') and len(document.get('skills')) > 0:
        for skill in document.get('skills'):
            # Check if a matching record exists
            query = """
                SELECT id
                FROM DIM_PRF_Trait
                WHERE type = %(type)s
                AND name = %(name)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'type': 'skill', 'name': skill})

            if not result.empty:
                # If matching record found, use existing id
                skill_id = result.iloc[0]['id']
            else:
                # If no matching record found, insert a new record and use its id
                pd.DataFrame([{
                    'type': 'skill',
                    'name': skill
                }]).to_sql('DIM_PRF_Trait', dwh_engine, if_exists='append', index=False)
                skill_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]

            # Check if a relationship record already exists
            query = """
                SELECT *
                FROM REL_PRF_Person_Trait
                WHERE idPerson = %(idPerson)s
                AND idTrait = %(idTrait)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'idPerson': person_id, 'idTrait': skill_id})

            # Insert if relationship record does not exist
            if result.empty:
                pd.DataFrame([{
                    'idPerson': person_id,
                    'idTrait': skill_id
                }]).to_sql('REL_PRF_Person_Trait', dwh_engine, if_exists='append', index=False)


def interests(document: dict, person_id: int, dwh_engine):
    """
    This function inserts interests into the DWH.

    DWH tables: DIM_PRF_Trait, REL_PRF_Person_Trait

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('interests') and len(document.get('interests')) > 0:
        for interest in document.get('interests'):
            # Check if a matching record exists
            query = """
                SELECT id
                FROM DIM_PRF_Trait
                WHERE type = %(type)s
                AND name = %(name)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'type': 'interest', 'name': interest})

            if not result.empty:
                # If matching record found, use existing id
                interest_id = result.iloc[0]['id']
            else:
                # If no matching record found, insert a new record and use its id
                pd.DataFrame([{
                    'type': 'interest',
                    'name': interest
                }]).to_sql('DIM_PRF_Trait', dwh_engine, if_exists='append', index=False)
                interest_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]

            # Check if a relationship record already exists
            query = """
                SELECT *
                FROM REL_PRF_Person_Trait
                WHERE idPerson = %(idPerson)s
                AND idTrait = %(idTrait)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'idPerson': person_id, 'idTrait': interest_id})

            # Insert if relationship record does not exist
            if result.empty:
                pd.DataFrame([{
                    'idPerson': person_id,
                    'idTrait': interest_id
                }]).to_sql('REL_PRF_Person_Trait', dwh_engine, if_exists='append', index=False)


def groups(document: dict, person_id: int, dwh_engine):
    """
    This function inserts groups into the DWH.

    DWH tables: DIM_PRF_Group, REL_PRF_Person_Group

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('groups') and len(document.get('groups')) > 0:
        for group in document.get('groups'):
            if group.get('name'):
                # Check if a matching record exists
                query = """
                    SELECT id
                    FROM DIM_PRF_Group
                    WHERE name = %(name)s
                """
                result = pd.read_sql_query(query, dwh_engine, params={'name': group.get('name')})

                if not result.empty:
                    # If matching record found, use existing id
                    group_id = result.iloc[0]['id']
                else:
                    # If no matching record found, insert a new record and use its id
                    pd.DataFrame([{
                        'name': group.get('name')
                    }]).to_sql('DIM_PRF_Group', dwh_engine, if_exists='append', index=False)
                    group_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]

                # Check if a relationship record already exists
                query = """
                    SELECT *
                    FROM REL_PRF_Person_Group
                    WHERE idPerson = %(idPerson)s
                    AND idGroup = %(idGroup)s
                """
                result = pd.read_sql_query(query, dwh_engine, params={'idPerson': person_id, 'idGroup': group_id})

                # Insert if relationship record does not exist
                if result.empty:
                    pd.DataFrame([{
                        'idPerson': person_id,
                        'idGroup': group_id
                    }]).to_sql('REL_PRF_Person_Group', dwh_engine, if_exists='append', index=False)


def experiences(document: dict, person_id: int, dwh_engine):
    """
    This function inserts experiences into the DWH.

    DWH tables: DIM_PRF_Duration, FACT_PRF_Qualification

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('experiences') and len(document.get('experiences')) > 0:
        for experience in document.get('experiences'):
            # Create and fill the duration dimension table
            if experience.get('starts_at') or experience.get('ends_at'):
                duration_df = pd.DataFrame([{
                    'startDate': conv.convert_date(experience.get('starts_at')),
                    'endDate': conv.convert_date(experience.get('ends_at'))
                }])
                # Check if matching records exist
                query = """
                    SELECT id
                    FROM DIM_PRF_Duration
                    WHERE startDate = %(startDate)s
                    AND endDate = %(endDate)s
                """
                result = pd.read_sql_query(query, dwh_engine, params=duration_df.iloc[0].to_dict())

                # If matching records found, use existing id
                if not result.empty:
                    duration_id = result.iloc[0]['id']
                else:
                    # If no matching records found, insert a new record and use its id
                    duration_df.to_sql('DIM_PRF_Duration', dwh_engine, if_exists='append', index=False)
                    duration_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]
            else:
                duration_id = None

            # Convert experience to FACT_PRF_Qualification table
            experience_df = conv.experience(experience, person_id, duration_id)

            # Insert experience data
            experience_df.to_sql('FACT_PRF_Qualification', dwh_engine, if_exists='append', index=False)


def education(document: dict, person_id: int, dwh_engine):
    """
    This function inserts education into the DWH.

    DWH tables: FACT_PRF_Qualification, DIM_PRF_Duration

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('education') and len(document.get('education')) > 0:
        for education in document.get('education'):
            # Create and fill the duration dimension table
            if education.get('starts_at') or education.get('ends_at'):
                duration_df = pd.DataFrame([{
                    'startDate': conv.convert_date(education.get('starts_at')),
                    'endDate': conv.convert_date(education.get('ends_at'))
                }])
                # Check if matching records exist
                query = """
                        SELECT id
                        FROM DIM_PRF_Duration
                        WHERE startDate = %(startDate)s
                        AND endDate = %(endDate)s
                    """
                result = pd.read_sql_query(query, dwh_engine, params=duration_df.iloc[0].to_dict())

                # If matching records found, use existing id
                if not result.empty:
                    duration_id = result.iloc[0]['id']
                else:
                    # If no matching records found, insert a new record and use its id
                    duration_df.to_sql('DIM_PRF_Duration', dwh_engine, if_exists='append', index=False)
                    duration_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]
            else:
                duration_id = None

            # Convert education to FACT_PRF_Qualification table
            education_df = conv.education(education, person_id, duration_id)

            # Insert education data
            education_df.to_sql('FACT_PRF_Qualification', dwh_engine, if_exists='append', index=False)


def volunteer_work(document: dict, person_id: int, dwh_engine):
    """
    This function inserts volunteer work into the DWH.

    DWH tables: FACT_PRF_Qualification, DIM_PRF_Duration

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('volunteer_work') and len(document.get('volunteer_work')) > 0:
        for volunteer in document.get('volunteer_work'):
            # Create and fill the duration dimension table
            if volunteer.get('starts_at') or volunteer.get('ends_at'):
                duration_df = pd.DataFrame([{
                    'startDate': conv.convert_date(volunteer.get('starts_at')),
                    'endDate': conv.convert_date(volunteer.get('ends_at'))
                }])
                # Check if matching records exist
                query = """
                    SELECT id
                    FROM DIM_PRF_Duration
                    WHERE startDate = %(startDate)s
                    AND endDate = %(endDate)s
                """
                result = pd.read_sql_query(query, dwh_engine, params=duration_df.iloc[0].to_dict())

                # If matching records found, use existing id
                if not result.empty:
                    duration_id = result.iloc[0]['id']
                else:
                    # If no matching records found, insert a new record and use its id
                    duration_df.to_sql('DIM_PRF_Duration', dwh_engine, if_exists='append', index=False)
                    duration_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]
            else:
                duration_id = None

            # Convert volunteer to FACT_PRF_Qualification table
            volunteer_df = conv.volunteer_work(volunteer, person_id, duration_id)

            # Insert volunteer data
            volunteer_df.to_sql('FACT_PRF_Qualification', dwh_engine, if_exists='append', index=False)
