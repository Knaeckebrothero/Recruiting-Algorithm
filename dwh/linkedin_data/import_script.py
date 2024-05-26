"""
This script is used to import LinkedIn data from the MongoDB database into the DWH.
"""
import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import pandas as pd
from sqlalchemy import create_engine  # Requires pymysql
from datetime import datetime
# Import conversion functions
from convert import profile as pf


# Load environment variables
load_dotenv(find_dotenv())

# !!!UNENCRYPTED CONNECTION ONLY USE ON LAN!!!
dwh_connection_url = os.getenv("DATABASE_DWH")
dwh = create_engine(dwh_connection_url)
mongodb = MongoClient(os.getenv("MongoClientURI"))["dwh_sources"]
collection = mongodb["KGL_LIN_PRF"]

# Load the collection
documents = collection.find({'public_identifier': 'tatiana-kapkan'})  # collection.find()

# Main loop
for doc in documents:
    # Prepare location data
    location_df = pf.location(doc)

    # Check if a matching record exists
    query = """
        SELECT id
        FROM DIM_LIN_Location
        WHERE countryLetters = %(countryLetters)s 
        AND countryName = %(countryName)s
        AND city = %(city)s
        AND state = %(state)s
    """
    result = pd.read_sql_query(query, dwh, params=location_df.iloc[0].to_dict())

    if not result.empty:
        # If matching record found, use existing id
        location_id = result.iloc[0]['id']
    else:
        # If no matching record found, insert a new record and use its id
        location_df.to_sql('DIM_LIN_Location', dwh, if_exists='append', index=False)
        location_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh).iloc[0, 0]

    # Prepare person data
    person_df = pf.person(doc, location_id, 10)

    # Insert person data
    person_df.to_sql('FACT_PRF_Person', dwh, if_exists='append', index=False)
    person_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh).iloc[0, 0]

    # Insert recommendation data
    if doc.get('recommendations') and len(doc.get('recommendations')) > 0:
        for rec in doc.get('recommendations'):
            # Create and insert recommendation
            pd.DataFrame({
                'idPerson': person_id,
                'recommendationText': rec
            }).to_sql('FACT_PRF_Recommendation', dwh, if_exists='append', index=False)
    
    # Insert people_also_viewed attribute into related profiles table
    if doc.get('people_also_viewed') and len(doc.get('people_also_viewed')) > 0:
        for related in doc.get('people_also_viewed'):
            # Create and insert profile
            pd.DataFrame({
                'idPerson': person_id,
                'type': 'viewed',
                'name': related.get('name'),
                'location': related.get('location'),
                'summary': related.get('summary')
            }).to_sql('FACT_PRF_Recommendation', dwh, if_exists='append', index=False)
    
    # Insert similarly_named_profiles attribute into related profiles table
    if doc.get('similarly_named_profiles') and len(doc.get('similarly_named_profiles')) > 0:
        for related in doc.get('similarly_named_profiles'):
            # Create and insert profile
            pd.DataFrame({
                'idPerson': person_id,
                'type': 'similar',
                'name': related.get('name'),
                'location': related.get('location'),
                'summary': related.get('summary')
            }).to_sql('FACT_PRF_Recommendation', dwh, if_exists='append', index=False)

    # Insert language data
    if doc.get('languages') and len(doc.get('languages')) > 0:
        for lang in doc.get('languages'):
            # Check if a matching record exists
            query = """
                SELECT id
                FROM DIM_PRF_Language
                WHERE language = %(language)s
            """
            result = pd.read_sql_query(query, dwh, params={'language': lang})

            if not result.empty:
                # If matching record found, use existing id
                lang_id = result.iloc[0]['id']
            else:
                # If no matching record found, insert a new record and use its id
                pd.DataFrame({
                    'language': lang
                }).to_sql('DIM_PRF_Language', dwh, if_exists='append', index=False)
                lang_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh).iloc[0, 0]

            # Check if a relationship record already exists
            query = """
                SELECT *
                FROM REL_PRF_Person_Language
                WHERE idPerson = %(idPerson)s
                AND idLanguage = %(idLanguage)s
            """
            result = pd.read_sql_query(query, dwh, params={'idPerson': person_id, 'idLanguage': lang_id})

            # Insert if relationship record does not exist
            if result.empty:
                pd.DataFrame({
                    'idPerson': person_id,
                    'idLanguage': lang_id
                }).to_sql('REL_PRF_Person_Language', dwh, if_exists='append', index=False)

        # Insert skills attribute into trait table
        if doc.get('skills') and len(doc.get('skills')) > 0:
            for skill in doc.get('skills'):
                # Check if a matching record exists
                query = """
                    SELECT id
                    FROM DIM_PRF_Trait
                    WHERE type = %(type)s
                    AND name = %(name)s
                """
                result = pd.read_sql_query(query, dwh, params={'type': 'skill', 'name': skill})

                if not result.empty:
                    # If matching record found, use existing id
                    skill_id = result.iloc[0]['id']
                else:
                    # If no matching record found, insert a new record and use its id
                    pd.DataFrame({
                        'type': 'skill',
                        'name': skill
                    }).to_sql('DIM_PRF_Trait', dwh, if_exists='append', index=False)
                    skill_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh).iloc[0, 0]

                # Check if a relationship record already exists
                query = """
                    SELECT *
                    FROM REL_PRF_Person_Trait
                    WHERE idPerson = %(idPerson)s
                    AND idTrait = %(idTrait)s
                """
                result = pd.read_sql_query(query, dwh, params={'idPerson': person_id, 'idTrait': skill_id})

                # Insert if relationship record does not exist
                if result.empty:
                    pd.DataFrame({
                        'idPerson': person_id,
                        'idTrait': skill_id
                    }).to_sql('REL_PRF_Person_Trait', dwh, if_exists='append', index=False)

    # Insert interests attribute into trait table
    if doc.get('interests') and len(doc.get('interests')) > 0:
        for interest in doc.get('interests'):
            # Check if a matching record exists
            query = """
                SELECT id
                FROM DIM_PRF_Trait
                WHERE type = %(type)s
                AND name = %(name)s
            """
            result = pd.read_sql_query(query, dwh, params={'type': 'interest', 'name': interest})

            if not result.empty:
                # If matching record found, use existing id
                interest_id = result.iloc[0]['id']
            else:
                # If no matching record found, insert a new record and use its id
                pd.DataFrame({
                    'type': 'interest',
                    'name': interest
                }).to_sql('DIM_PRF_Trait', dwh, if_exists='append', index=False)
                interest_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh).iloc[0, 0]

            # Check if a relationship record already exists
            query = """
                SELECT *
                FROM REL_PRF_Person_Trait
                WHERE idPerson = %(idPerson)s
                AND idTrait = %(idTrait)s
            """
            result = pd.read_sql_query(query, dwh, params={'idPerson': person_id, 'idTrait': interest_id})

            # Insert if relationship record does not exist
            if result.empty:
                pd.DataFrame({
                    'idPerson': person_id,
                    'idTrait': interest_id
                }).to_sql('REL_PRF_Person_Trait', dwh, if_exists='append', index=False)

    # Insert groups
    if doc.get('groups') and len(doc.get('groups')) > 0:
        for group in doc.get('groups'):
            if group.get('name'):
                # Check if a matching record exists
                query = """
                    SELECT id
                    FROM DIM_PRF_Group
                    WHERE name = %(name)s
                """
                result = pd.read_sql_query(query, dwh, params={'name': group.get('name')})

                if not result.empty:
                    # If matching record found, use existing id
                    group_id = result.iloc[0]['id']
                else:
                    # If no matching record found, insert a new record and use its id
                    pd.DataFrame({
                        'name': group.get('name')
                    }).to_sql('DIM_PRF_Group', dwh, if_exists='append', index=False)
                    group_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh).iloc[0, 0]

                # Check if a relationship record already exists
                query = """
                    SELECT *
                    FROM REL_PRF_Person_Group
                    WHERE idPerson = %(idPerson)s
                    AND idGroup = %(idGroup)s
                """
                result = pd.read_sql_query(query, dwh, params={'idPerson': person_id, 'idGroup': group_id})

                # Insert if relationship record does not exist
                if result.empty:
                    pd.DataFrame({
                        'idPerson': person_id,
                        'idGroup': group_id
                    }).to_sql('REL_PRF_Person_Group', dwh, if_exists='append', index=False)

    # Insert qualifications
      !!!  START WITH EXPERIENCE HERE !!!
        pf.experience(doc.get('experience'), person_id)
