"""
This script is used to import LinkedIn data from the MongoDB database into the DWH.
"""
import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine  # Requires pymysql
import concurrent.futures
from dwh.linkedin_data.profiles import insert  # Import insertion functions


# Put the insertion logic into a function, so it can be used with multithreading
def insert_collection_documents(
        collection_str: str,
        id_origin: int,
        dwh_connection_url: str,
        mongo_connection_url: str,
        schema_name: str = 'DWH1'
       ):
    # Add charset to sql connection string to avoid encoding issues
    dwh = create_engine(f'{dwh_connection_url}/{schema_name}?charset=utf8mb4')  # echo=True for debugging

    # Connect to the MongoDB database
    mongodb = MongoClient(mongo_connection_url)["raw_data"]
    collection = mongodb[collection_str]

    # Initialize counter variables
    counter = 0
    total = collection.count_documents({})

    # Get the collection cursor
    documents = collection.find()

    # Insertion loop
    for doc in documents:
        try:
            # Print progress
            counter += 1
            print(f"{collection_str}: {counter}/{total}")

            # Skip documents without experiences
            if not doc.get('experiences', []):
                continue

            # Insert the document into the DWH and get the ids
            key_of_location = insert.location(doc, dwh)  # Insert location
            key_of_person = insert.person(doc, key_of_location, id_origin, dwh)  # Insert person

            # Insert the rest of the data
            insert.recommendations(doc, key_of_person, dwh)  # Insert recommendations
            # insert.people_also_viewed(doc, key_of_person, dwh)  # Insert people_also_viewed
            # insert.similarly_named_profiles(doc, key_of_person, dwh)  # Insert similarly_named_profiles
            insert.languages(doc, key_of_person, dwh)  # Insert languages
            insert.skills(doc, key_of_person, dwh)  # Insert skills
            insert.interests(doc, key_of_person, dwh)  # Insert interests
            insert.groups(doc, key_of_person, dwh)  # Insert groups
            insert.experiences(doc, key_of_person, dwh)  # Insert experiences
            insert.education(doc, key_of_person, dwh)  # Insert education
            insert.volunteer_work(doc, key_of_person, dwh)  # Insert volunteer_work
            insert.certifications(doc, key_of_person, dwh)  # Insert certifications
            insert.activities(doc, key_of_person, dwh)  # Insert activities
            insert.articles(doc, key_of_person, dwh)  # Insert articles
            insert.accomplishment_organisations(doc, key_of_person, dwh)  # Insert accomplishment_organisations
            insert.accomplishment_publications(doc, key_of_person, dwh)  # Insert accomplishment_publications
            insert.accomplishment_honors_awards(doc, key_of_person, dwh)  # Insert accomplishment_honors_awards
            insert.accomplishment_patents(doc, key_of_person, dwh)  # Insert accomplishment_patents
            insert.accomplishment_test_scores(doc, key_of_person, dwh)  # Insert accomplishment_test_scores
            insert.accomplishment_courses(doc, key_of_person, dwh)  # Insert accomplishment_courses
            insert.accomplishment_projects(doc, key_of_person, dwh)  # Insert accomplishment_projects
        except Exception as e:
            print(f"Error: {doc['_id']}")
            print(e)


# Load environment variables
load_dotenv(find_dotenv())

# MySQLs connection string
mysql_url = os.getenv("DATABASE_DWH")

# MongoDBs connection string
mongo_url = os.getenv("MongoClientURI")

# Define the schema name, collection name, and the origin ID
dwh_schema_name = 'DWH'
mongo_collection_name = "KGL_LIN_PRF_USA"
dwh_id_origin = 1

collections = [
    {"name": "KGL_LIN_PRF_USA", "id_origin": 1},
    {"name": "KGL_LIN_PRF_IND", "id_origin": 2},
    {"name": "KGL_LIN_PRF_CAN", "id_origin": 3},
    {"name": "KGL_LIN_PRF_SNG", "id_origin": 4},  # Works
    {"name": "KGL_LIN_PRF_ISR", "id_origin": 5},
    {"name": "KGL_LIN_PRF_BRS", "id_origin": 6},
    {"name": "KGL_LIN_PRF_JPN", "id_origin": 7},
    {"name": "KGL_LIN_PRF_DEN", "id_origin": 8}
]

"""
# Run the insertion function
insert_collection_documents(
    mongo_collection_name,
    dwh_id_origin,
    mysql_url,
    mongo_url,
    dwh_schema_name
)
"""

# Create a ThreadPoolExecutor with 4 worker threads
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    # Submit the insertion tasks to the executor
    futures = [
        executor.submit(
            insert_collection_documents,
            collection["name"],
            collection["id_origin"],
            mysql_url,
            mongo_url,
            dwh_schema_name,
        )
        for collection in collections
    ]

    # Keep track of failed tasks
    failed_tasks = []

    # Retrieve the results and handle exceptions
    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
            print(f"Task completed successfully: {result}")
        except Exception as e:
            print(f"Task encountered an exception: {e}")
            failed_tasks.append(future)

# Display a summary of failed tasks
if failed_tasks:
    print("\nSummary of failed tasks:")
    for task in failed_tasks:
        print(f"- Task: {task}")
else:
    print("\nAll tasks completed successfully.")
