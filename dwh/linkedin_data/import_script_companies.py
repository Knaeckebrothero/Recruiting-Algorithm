"""
This script is used to import LinkedIn data from the MongoDB database into the DWH.
"""
import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine  # Requires pymysql

# Import insertion functions
from dwh.linkedin_data.companies import insert


# Load environment variables
load_dotenv(find_dotenv())

# !!!UNENCRYPTED CONNECTION ONLY USE ON LAN!!!
dwh_connection_url = os.getenv("DATABASE_DWH")
# Add charset to connection string to avoid encoding issues
dwh = create_engine(dwh_connection_url + '/DWH?charset=utf8mb4')  # dwh = create_engine(dwh_connection_url,
# echo=True)
mongodb = MongoClient(os.getenv("MongoClientURI"))["raw_data"]

# Get the collection details
collection = mongodb["KGL_LIN_"]
id_origin = 0

# Initialize counter variables
counter = 0
total = collection.count_documents({})

# Get the collection cursor
documents = collection.find()  # collection.find()

# Main loop
for doc in documents:
    # Print progress
    counter += 1
    print(f"Document: {counter}/{total}")

    # Insert location and get its ID
    hq_location_id = insert.hq_location(doc, dwh)

    # Insert company and get its ID
    company_id = insert.company(doc, hq_location_id, id_origin, dwh)

    # Insert updates
    insert.updates(doc, company_id, dwh)

    # Insert similar_companies
    insert.similar_companies(doc, company_id, dwh)

    # Insert specialties
    insert.specialties(doc, company_id, dwh)

    # Insert locations
    insert.locations(doc, company_id, dwh)
