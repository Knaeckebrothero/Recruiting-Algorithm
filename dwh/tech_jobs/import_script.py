"""
This script is used to import job data from the MongoDB database into the DWH.
"""
import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine  # Requires pymysql
import pandas as pd


def build_dimension_table(mongo_collection):
    """
    This function builds the dimension table for skills from the MongoDB collection.
    :param mongo_collection: The MongoDB collection to build the dimension table from.
    :return: A DataFrame of unique skills.
    """
    unique_skills = set()

    # Iterate over each document in the collection
    for document in collection.find():
        # Check if the "HaveWorkedWith" attribute exists in the document
        if "HaveWorkedWith" in document:
            skills = document["HaveWorkedWith"].split(";")
            unique_skills.update(skills)

    # Return the set of unique skills as a pandas DataFrame
    return pd.DataFrame(list(unique_skills), columns=["name"])


def convert_person(document):
    """
    This function converts a person document from the MongoDB collection to a person record for the DWH.
    :param document: The person document from the MongoDB collection.
    :return: A person record for the DWH.
    """
    # Determine gender
    match document.get('Gender'):
        case "Woman":
            gender_bool = 1
        case "Man":
            gender_bool = 0
        case _:
            # Includes NonBinary value
            gender_bool = None

    # Initialize the person record
    person = {
        'educationLevel': document.get('educationLevel'),
        'country': document.get('Country'),
        'salary': int(round(float(document.get('PreviousSalary')))),
        'yearsCode': document.get('YearsCode'),
        'gender': gender_bool,
        'age': document.get('Age'),
        'isDev': 1 if document.get('MainBranch') == 'Dev' else 0,

    }

    # Return the person record as a pandas DataFrame
    return pd.DataFrame([person])


# Load environment variables
load_dotenv(find_dotenv())

# !!!UNENCRYPTED CONNECTION ONLY USE ON LAN!!!
dwh_connection_url = os.getenv("DATABASE_DWH")
# Add charset to connection string to avoid encoding issues
dwh = create_engine(dwh_connection_url + '/DWH1?charset=utf8mb4')  # dwh = create_engine(dwh_connection_url,
# echo=True)
mongodb = MongoClient(os.getenv("MongoClientURI"))["raw_data"]

# Get the collection details
collection = mongodb["KGL_LIN_PRF"]
id_origin = 0

# Initialize counter variables
counter = 0
total = collection.count_documents({})

# Get the collection cursor
documents = collection.find()

# Insert the dimension table for skills
skills = build_dimension_table(collection)
skills.to_sql("DIM_TJS_Skill", dwh, if_exists="append", index=False)

# Get the dimension table for skills
skills = pd.read_sql("SELECT * FROM DIM_TJS_Skill", dwh)

# Main loop
for doc in documents:
    # Print progress
    counter += 1
    print(f"Document: {counter}/{total}")

    #
    if document.get('recommendations'):
        df_to_add = document.get('recommendations', [])
        data = []

        # Populate list with data
        for rec in df_to_add:
            data.append({
                'idPerson': person_id,
                'recommendationText': rec
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Recommendation', dwh_engine, if_exists='append', index=False)



