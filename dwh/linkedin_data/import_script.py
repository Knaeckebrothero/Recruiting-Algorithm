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
# Add charset to connection string to avoid encoding issues
dwh = create_engine(dwh_connection_url + '?charset=utf8mb4')  # dwh = create_engine(dwh_connection_url, echo=True)
mongodb = MongoClient(os.getenv("MongoClientURI"))["dwh_sources"]
collection = mongodb["KGL_LIN_PRF"]

# Initialize counter variables
counter = 0
total = collection.count_documents({})

# Get the collection cursor
documents = collection.find({'public_identifier': 'tatiana-kapkan'})  # collection.find()

# Main loop
for doc in documents:
    # Print progress
    counter += 1
    print(f"Document: {counter}/{total}")

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
    person_df = pf.person(doc, location_id, 2)

    # Insert person data
    person_df.to_sql('FACT_PRF_Person', dwh, if_exists='append', index=False)
    person_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh).iloc[0, 0]

    # Insert recommendation data
    if doc.get('recommendations'):
        recommendations = doc.get('recommendations', [])
        data = []

        # Populate list with data
        for rec in recommendations:
            data.append({
                'idPerson': person_id,
                'recommendationText': rec
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Recommendation', dwh, if_exists='append', index=False)

    # Insert people_also_viewed attribute into related profiles table
    if doc.get('people_also_viewed'):
        df_to_add = doc.get('people_also_viewed', [])
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
            pd.DataFrame(data).to_sql('FACT_PRF_Related', dwh, if_exists='append', index=False)
    
    # Insert similarly_named_profiles attribute into related profiles table
    if doc.get('similarly_named_profiles'):
        df_to_add = doc.get('similarly_named_profiles', [])
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
            pd.DataFrame(data).to_sql('FACT_PRF_Related', dwh, if_exists='append', index=False)

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
                    'language': [lang]
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
                pd.DataFrame([{
                    'idPerson': person_id,
                    'idLanguage': lang_id
                }]).to_sql('REL_PRF_Person_Language', dwh, if_exists='append', index=False)

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
                    pd.DataFrame([{
                        'type': 'skill',
                        'name': skill
                    }]).to_sql('DIM_PRF_Trait', dwh, if_exists='append', index=False)
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
                    pd.DataFrame([{
                        'idPerson': person_id,
                        'idTrait': skill_id
                    }]).to_sql('REL_PRF_Person_Trait', dwh, if_exists='append', index=False)

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
                pd.DataFrame([{
                    'type': 'interest',
                    'name': interest
                }]).to_sql('DIM_PRF_Trait', dwh, if_exists='append', index=False)
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
                pd.DataFrame([{
                    'idPerson': person_id,
                    'idTrait': interest_id
                }]).to_sql('REL_PRF_Person_Trait', dwh, if_exists='append', index=False)

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
                    pd.DataFrame([{
                        'name': group.get('name')
                    }]).to_sql('DIM_PRF_Group', dwh, if_exists='append', index=False)
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
                    pd.DataFrame([{
                        'idPerson': person_id,
                        'idGroup': group_id
                    }]).to_sql('REL_PRF_Person_Group', dwh, if_exists='append', index=False)

    # Insert experiences attribute into qualification table
    if doc.get('experiences') and len(doc.get('experiences')) > 0:
        for experience in doc.get('experiences'):
            # Create and fill the duration dimension table
            if experience.get('starts_at') or experience.get('ends_at'):
                duration_df = pd.DataFrame([{
                    'startDate': pf.convert_date(experience.get('starts_at')),
                    'endDate': pf.convert_date(experience.get('ends_at'))
                }])
                # Check if matching records exist
                query = """
                    SELECT id
                    FROM DIM_PRF_Duration
                    WHERE startDate = %(startDate)s
                    AND endDate = %(endDate)s
                """
                result = pd.read_sql_query(query, dwh, params=duration_df.iloc[0].to_dict())

                # If matching records found, use existing id
                if not result.empty:
                    duration_id = result.iloc[0]['id']
                else:
                    # If no matching records found, insert a new record and use its id
                    duration_df.to_sql('DIM_PRF_Duration', dwh, if_exists='append', index=False)
                    duration_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh).iloc[0, 0]
            else:
                duration_id = None

            # Create and fill the institution dimension table
            if experience.get('company') or experience.get('location'):
                institution_df = pd.DataFrame([{
                    'name': experience.get('company'),
                    'location': experience.get('location')
                }])
                # Check if matching records exist
                query = """
                    SELECT id
                    FROM DIM_PRF_Institution
                    WHERE name = %(name)s
                    AND location = %(location)s
                """
                result = pd.read_sql_query(query, dwh, params=institution_df.iloc[0].to_dict())

                # If matching records found, use existing id
                if not result.empty:
                    institution_id = result.iloc[0]['id']
                else:
                    # If no matching records found, insert a new record and use its id
                    institution_df.to_sql('DIM_PRF_Institution', dwh, if_exists='append', index=False)
                    institution_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh).iloc[0, 0]
            else:
                institution_id = None

            # Convert experience to FACT_PRF_Qualification table
            experience_df = pf.experience(experience, person_id, duration_id, institution_id)

            # Insert experience data
            experience_df.to_sql('FACT_PRF_Qualification', dwh, if_exists='append', index=False)

    # Insert education attribute into qualification table
    if doc.get('education') and len(doc.get('education')) > 0:
            for education in doc.get('education'):
                # Create and fill the duration dimension table
                if education.get('starts_at') or education.get('ends_at'):
                    duration_df = pd.DataFrame([{
                        'startDate': pf.convert_date(education.get('starts_at')),
                        'endDate': pf.convert_date(education.get('ends_at'))
                    }])
                    # Check if matching records exist
                    query = """
                        SELECT id
                        FROM DIM_PRF_Duration
                        WHERE startDate = %(startDate)s
                        AND endDate = %(endDate)s
                    """
                    result = pd.read_sql_query(query, dwh, params=duration_df.iloc[0].to_dict())

                    # If matching records found, use existing id
                    if not result.empty:
                        duration_id = result.iloc[0]['id']
                    else:
                        # If no matching records found, insert a new record and use its id
                        duration_df.to_sql('DIM_PRF_Duration', dwh, if_exists='append', index=False)
                        duration_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh).iloc[0, 0]
                else:
                    duration_id = None

                # Create and fill the institution dimension table
                if education.get('school'):
                    institution_df = pd.DataFrame([{
                        'name': education.get('institution'),
                        'location': None
                    }])
                    # Check if matching records exist
                    query = """
                        SELECT id
                        FROM DIM_PRF_Institution
                        WHERE name = %(name)s
                        AND location = %(location)s
                    """
                    result = pd.read_sql_query(query, dwh, params=institution_df.iloc[0].to_dict())

                    # If matching records found, use existing id
                    if not result.empty:
                        institution_id = result.iloc[0]['id']
                    else:
                        # If no matching records found, insert a new record and use its id
                        institution_df.to_sql('DIM_PRF_Institution', dwh, if_exists='append', index=False)
                        institution_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh).iloc[0, 0]
                else:
                    institution_id = None

                # Convert education to FACT_PRF_Qualification table
                education_df = pf.education(education, person_id, duration_id, institution_id)
