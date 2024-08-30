"""
This script holds the main function for the tagging pipeline.
"""
import os
import pymongo
import json
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from bson import ObjectId
from langchain_openai import ChatOpenAI
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult

from custom_logger import configure_custom_logger
from preprocess import clean_text
from process.generate import apply_tag_generation_to_dataframe


class DetailedCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.request_data = {}
        self.response_data = {}

    def on_llm_start(self, serialized: dict[str, any], prompts: list[str], **kwargs: any) -> None:
        self.request_data = {
            "model": serialized.get("name"),
            "prompts": prompts,
            "invocation_params": serialized.get("invocation_params", {})
        }

    def on_llm_end(self, response: LLMResult, **kwargs: any) -> None:
        self.response_data = {
            "generations": [
                [
                    {
                        "text": gen.text,
                        "generation_info": gen.generation_info,
                        "type": gen.type
                    } for gen in gens
                ] for gens in response.generations
            ],
            "llm_output": response.llm_output
        }


def get_total_profile_count(mongo_client, mongo_collection_name, database, mongo_query=None):
    """
    Get the total number of profiles that have experiences or education data.

    :param mongo_client: MongoDB client object
    :param mongo_collection_name: Name of the MongoDB collection
    :param database: Name of the MongoDB database
    :param mongo_query: Optional query to filter profiles

    :return: Total number of profiles
    """
    db = mongo_client[database]
    collection = db[mongo_collection_name]

    # Query to find profiles with experiences or education data
    if not mongo_query:
        return collection.count_documents({})
    else:
        return collection.count_documents(mongo_query)


def load_profiles(
        mongo_client, mongo_collection_name, profiles_to_skip, limit, database,
        mongo_query=None, mongo_projection=None):
    """
    Load profiles that have experiences or education data from the MongoDB collection.

    :param mongo_client: MongoDB client object
    :param mongo_collection_name: Name of the MongoDB collection
    :param profiles_to_skip: Number of profiles to skip
    :param limit: Maximum number of profiles to load
    :param database: Name of the MongoDB database
    :param mongo_query: Optional query to filter profiles
    :param mongo_projection: Optional projection to include only necessary fields

    :return: DataFrame containing the loaded profiles
    """
    if mongo_projection is None:
        mongo_projection = {}
    if mongo_query is None:
        mongo_query = {}

    db = mongo_client[database]
    collection = db[mongo_collection_name]

    # Load profiles using the query, projection, skip, and limit
    profiles = list(collection.find(mongo_query, mongo_projection).skip(profiles_to_skip).limit(limit))

    # Return the profiles as a DataFrame
    return pd.DataFrame(profiles)


def save_results(client, mongo_collection_name, dataframe, database):
    """
    Save the processed results to the MongoDB collection.

    :param client: MongoDB client object
    :param mongo_collection_name: Name of the MongoDB collection
    :param dataframe: DataFrame containing the processed results
    :param database: Name of the MongoDB database
    """
    client[database][mongo_collection_name].insert_many(dataframe.to_dict('records'))
    """
    for result in results:
        # Ensure _id is an ObjectId
        if not isinstance(result['_id'], ObjectId):
            result['_id'] = ObjectId(result['_id'])

        # Insert the document, or update if it already exists
        collection.replace_one({'_id': result['_id']}, result, upsert=True)
    """


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    log = configure_custom_logger(module_name=__name__, logging_directory=os.getenv('LOGGING_DIRECTORY'))
    log.info("Environment variables loaded, logger initialized.")

    # Connect to MongoDB
    log.info("Connecting to MongoDB...")
    mongodb_client = pymongo.MongoClient(os.getenv('MONGO_CLIENT_URI'))

    # Define constants
    database_name = os.getenv('MONGO_DATABASE_NAME')
    collection_name = os.getenv('MONGO_COLLECTION_NAME')
    result_collection_name = os.getenv('MONGO_COLLECTION_NAME_RESULT')
    batch_size = int(os.getenv('BATCH_SIZE'))

    # Initialize the callback handler
    handler = DetailedCallbackHandler()

    # Load the model and template
    model = ChatOpenAI(
        model=os.getenv('MODEL_NAME'),
        temperature=0,
        seed=42,
        n=1,
    )

    # Load the template from the prompts.json file
    with open("prompts.json") as f:
        template = json.load(f)['experiences_template']
        f.close()

    # Query to find profiles with experiences or education data
    query = {
        "$or": [
            {"description": {"$exists": True, "$ne": []}}
        ]
    }

    # Projection to include only the necessary fields
    projection = {
        "_id": 0,
        "original_doc_id": 1,
        "company": 1,
        "title": 1,
        "description": 1,
    }

    try:
        # Get total number of profiles
        total_profiles = get_total_profile_count(mongodb_client, collection_name, database_name, query)
        log.info(f"Total profiles to process: {total_profiles}")

        # Process profiles in batches
        for skip in range(0, total_profiles, batch_size):
            df = load_profiles(
                mongodb_client, collection_name, skip, batch_size, database_name, query, projection)
            log.info(f"Loaded {len(df)} profiles (batch starting at {skip})")

            # Clean the text in the DataFrame
            df = df.map(clean_text)

            # Apply the preprocessing function
            df = apply_tag_generation_to_dataframe(df, model, template, handler)

            # Save the results to MongoDB
            save_results(mongodb_client, result_collection_name, df, database_name)
            log.info(f"Batch processed and saved (profiles {skip} to {skip + len(df) - 1})")

        # Log when all batches are processed
        log.info("All batches processed successfully")

    finally:
        # Close MongoDB connection
        log.info("Closing MongoDB connection...")
        mongodb_client.close()
        log.info("MongoDB connection closed, finished execution.")
