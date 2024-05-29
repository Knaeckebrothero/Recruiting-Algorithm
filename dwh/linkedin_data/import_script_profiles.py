"""
This script is used to import LinkedIn data from the MongoDB database into the DWH.
"""
import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine  # Requires pymysql

# Import insertion functions
from dwh.linkedin_data.profiles import insert


# Load environment variables
load_dotenv(find_dotenv())

# !!!UNENCRYPTED CONNECTION ONLY USE ON LAN!!!
dwh_connection_url = os.getenv("DATABASE_DWH")
# Add charset to connection string to avoid encoding issues
dwh = create_engine(dwh_connection_url + '/DWH?charset=utf8mb4')  # dwh = create_engine(dwh_connection_url, echo=True)
mongodb = MongoClient(os.getenv("MongoClientURI"))["raw_data"]

# Get the collection details
collection = mongodb["KGL_LIN_PRF_DEN"]
id_origin = 2

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

    # Insert location
    location_id = insert.location(doc, dwh)

    # Insert person
    person_id = insert.person(doc, location_id, id_origin, dwh)

    # Insert recommendations
    insert.recommendations(doc, person_id, dwh)

    # Insert people_also_viewed
    insert.people_also_viewed(doc, person_id, dwh)

    # Insert similarly_named_profiles
    insert.similarly_named_profiles(doc, person_id, dwh)
 
    # Insert languages
    insert.languages(doc, person_id, dwh)

    # Insert skills
    insert.skills(doc, person_id, dwh)

    # Insert interests
    insert.interests(doc, person_id, dwh)

    # Insert groups
    insert.groups(doc, person_id, dwh)
    
    # Insert experiences
    insert.experiences(doc, person_id, dwh)

    # Insert education
    insert.education(doc, person_id, dwh)

    # Insert volunteer_work
    insert.volunteer_work(doc, person_id, dwh)
    
    # Insert certifications
    insert.certifications(doc, person_id, dwh)

    # Insert activities
    insert.activities(doc, person_id, dwh)

    # Insert articles
    insert.articles(doc, person_id, dwh)

    # Insert accomplishment_organisations
    insert.accomplishment_organisations(doc, person_id, dwh)

    # Insert accomplishment_publications
    insert.accomplishment_publications(doc, person_id, dwh)

    # Insert accomplishment_honors_awards
    insert.accomplishment_honors_awards(doc, person_id, dwh)

    # Insert accomplishment_patents
    insert.accomplishment_patents(doc, person_id, dwh)

    # Insert accomplishment_test_scores
    insert.accomplishment_test_scores(doc, person_id, dwh)

    # Insert accomplishment_courses
    insert.accomplishment_courses(doc, person_id, dwh)

    # Insert accomplishment_projects
    insert.accomplishment_projects(doc, person_id, dwh)
