"""
This module holds the functions used to import the individual attributes into the DWH.
"""
import pandas as pd
import sqlalchemy  # Requires pymysql
from datetime import datetime
# Import conversion functions
from dwh.linkedin_data.companies import convert as conv


def hq_location(document: dict, dwh_engine):
    """
    This function inserts a location into the DWH and returns its ID.

    DWH table: DIM_LIN_Location

    :param document: The document to convert.
    :param dwh_engine: The DWH engine to use.
    """
    # Get the location data
    hq_dict = document.get('hq')

    # Prepare location data
    if hq_dict:
        location_df = conv.location(hq_dict)

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
    else:
        # Return None if no location data
        return None


def company(document: dict, hq_id: int, origin_id: int, dwh_engine) -> int:
    """
    This function inserts a person into the DWH and returns its ID.

    DWH table: FACT_PRF_Person

    :param document: The document to convert.
    :param hq_id: The ID of the hq location.
    :param origin_id: The ID of the DIM_Origin table from the dwh.
    :param dwh_engine: The DWH engine to use.
    """
    # Prepare person data
    company_df = conv.company(document, hq_id, origin_id)

    # Insert person data
    company_df.to_sql('FACT_CMP_Company', dwh_engine, if_exists='append', index=False)
    company_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]

    # Return person id
    return company_id


def updates(document: dict, company_id: int, dwh_engine):
    """
    This function inserts updates into the DWH.

    DWH table: FACT_LIN_CompanyUpdates

    :param document: The document to convert.
    :param company_id: The ID of


    # Check if updates exist
    if document.get('updates') & len(document.get('updates')) > 0:
        # Prepare update data
        updates_df = conv.updates(document, company_id)

        # Insert update data
        updates_df.to_sql('FACT_LIN_CompanyUpdates', dwh_engine, if_exists='append', index=False)


    """
    if document.get('updates'):
        df_to_add = document.get('updates', [])
        data = []

        # Populate list with data
        for update in df_to_add:
            data.append({
                'idCompany': company_id,
                'image': 1 if update.get('image') else 0,
                'postedOn': conv.convert_date(update.get('posted_on')),
                'likes': update.get('total_likes'),
                'text': update.get('text')
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_CMP_Update', dwh_engine, if_exists='append', index=False)


def similar_companies(document: dict, company_id: int, dwh_engine):
    """
    This function inserts similar companies into the DWH.

    DWH table: FACT_CMP_Similar

    :param document: The document to convert.
    :param company_id: The ID of the company in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('similar_companies'):
        df_to_add = document.get('similar_companies', [])
        data = []

        # Populate list with data
        for sim_company in df_to_add:
            data.append({
                'idCompany': company_id,
                'name': sim_company.get('name'),
                'industry': sim_company.get('industry'),
                'location': sim_company.get('location')
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_CMP_Similar', dwh_engine, if_exists='append', index=False)


def specialties(document: dict, company_id: int, dwh_engine):
    """
    This function inserts specialties into the DWH.

    DWH tables: DIM_CMP_Specialty, REL_CMP_Company_Specialty

    :param document: The document to convert.
    :param company_id: The ID of the company in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('specialities'):
        for spec in document.get('specialities'):
            # Check if a matching record exists
            query = """
                SELECT id
                FROM DIM_CMP_Specialty
                WHERE name = %(name)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'name': spec.strip()})

            if not result.empty:
                # If matching record found, use existing id
                spec_id = result.iloc[0]['id']
            else:
                # If no matching record found, insert a new record and use its id
                pd.DataFrame([{
                    'name': spec.strip()
                }]).to_sql('DIM_CMP_Specialty', dwh_engine, if_exists='append', index=False)
                spec_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]

            # Check if a relationship record already exists
            query = """
                SELECT *
                FROM REL_CMP_Company_Specialty
                WHERE idCompany = %(idCompany)s
                AND idSpecialty = %(idSpecialty)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'idCompany': company_id, 'idSpecialty': spec_id})

            # Insert if relationship record does not exist
            if result.empty:
                pd.DataFrame([{
                    'idCompany': company_id,
                    'idSpecialty': spec_id
                }]).to_sql('REL_CMP_Company_Specialty', dwh_engine, if_exists='append', index=False)

def locations(document: dict, company_id: int, dwh_engine):
    """
    This function inserts locations into the DWH.

    DWH tables: DIM_LIN_Location, REL_CMP_Company_Location

    :param document: The document to convert.
    :param company_id: The ID of the company in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('locations'):
        for loc in document.get('locations'):
            # Prepare location data
            location_df = conv.location(loc)

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

            # Check if a relationship record already exists
            query = """
                SELECT *
                FROM REL_CMP_Company_Location
                WHERE idCompany = %(idCompany)s
                AND idLocation = %(idLocation)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'idCompany': company_id, 'idLocation': location_id})

            # Insert if relationship record does not exist
            if result.empty:
                pd.DataFrame([{
                    'idCompany': company_id,
                    'idLocation': location_id
                }]).to_sql('REL_CMP_Company_Location', dwh_engine, if_exists='append', index=False)
