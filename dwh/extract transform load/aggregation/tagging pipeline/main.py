"""
This script holds the main function for the tagging pipeline.
"""
import os
import pymongo
import pandas as pd
import json
import logging
from dotenv import load_dotenv, find_dotenv
from bson import ObjectId

from preprocess import preprocess_data
from generate import generate_attributes
from postprocess import postprocess_data


def configure_custom_logger(
        module_name: str,  # = __name__,
        console_level: int = 20,
        file_level: int = 20,
        logging_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        logging_directory: str | None = None,
        separate_log_file: bool = False
        ) -> logging.Logger:
    """
    This function configures a custom logger for printing and saving logs in a logfile.

    :param module_name: Name for the logging module, could be __name__ or a custom name.
    :param console_level: The logging level for logging in the console.
    :param file_level: The logging level for logging in the logfile.
    :param logging_format: Format used for logging.
    :param logging_directory: Path for the directory where the log files should be saved to.
    :param separate_log_file: If True, a separate log file will be created for this logger.

    :return: A configured logger object.
    """
    logger = logging.getLogger(logging.getLoggerClass().root.name + "." + module_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(logging_format)

    # Set and create the logging directory if it does not exist
    if logging_directory is None:
        logging_directory = './config/logs/'
    if not os.path.exists(logging_directory):
        os.makedirs(logging_directory)

    # File handler for writing logs to a file
    if separate_log_file:
        file_handler = logging.FileHandler(logging_directory + module_name + '.log')
    else:
        file_handler = logging.FileHandler(logging_directory + 'main_log.log')

    file_handler.setFormatter(formatter)
    file_handler.setLevel(file_level)
    logger.addHandler(file_handler)

    # TODO: Store logs in database log level

    # Console (stream) handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(console_level)
    logger.addHandler(console_handler)

    return logger


def get_total_profile_count(mongo_client, mongo_collection_name, database):
    """
    Get the total number of profiles that have experiences or education data.

    :param mongo_client: MongoDB client object
    :param mongo_collection_name: Name of the MongoDB collection
    :param database: Name of the MongoDB database

    :return: Total number of profiles
    """
    db = mongo_client[database]
    collection = db[mongo_collection_name]

    # Query to find profiles with experiences or education data
    query = {
        "$or": [
            {"experiences": {"$exists": True, "$ne": []}},
            {"education": {"$exists": True, "$ne": []}}
        ]
    }

    return collection.count_documents(query)


def load_profiles(mongo_client, mongo_collection_name, skip, limit, database):
    """
    Load profiles that have experiences or education data from the MongoDB collection.

    :param mongo_client: MongoDB client object
    :param mongo_collection_name: Name of the MongoDB collection
    :param skip: Number of profiles to skip
    :param limit: Maximum number of profiles to load
    :param database: Name of the MongoDB database

    :return: DataFrame containing the loaded profiles
    """
    db = mongo_client[database]
    collection = db[mongo_collection_name]

    # Query to find profiles with experiences or education data
    query = {
        "$or": [
            {"experiences": {"$exists": True, "$ne": []}},
            {"education": {"$exists": True, "$ne": []}}
        ]
    }

    # Projection to include only the necessary fields
    projection = {
        "_id": 1,
        "experiences": 1,
        "education": 1
    }

    # Load profiles using the query, projection, skip, and limit
    profiles = list(collection.find(query, projection).skip(skip).limit(limit))
    return pd.DataFrame(profiles)


def save_results(client, mongo_collection_name, df, database):
    """
    Save the processed results to the MongoDB collection.

    :param client: MongoDB client object
    :param mongo_collection_name: Name of the MongoDB collection
    :param df: DataFrame containing the processed results
    :param database: Name of the MongoDB database
    """
    db = client[database]
    collection = db[mongo_collection_name]
    results = df.to_dict('records')

    for result in results:
        # Ensure _id is an ObjectId
        if not isinstance(result['_id'], ObjectId):
            result['_id'] = ObjectId(result['_id'])

        # Insert the document, or update if it already exists
        collection.replace_one({'_id': result['_id']}, result, upsert=True)

    logging.info(f"Saved {len(results)} results to the database.")


def process_batch(client, collection_name_data, collection_name_result, skip,
                  limit, experience_prompt, education_prompt, database):
    """
    Process a batch of profiles from the MongoDB collection.

    :param client: MongoDB client object
    :param collection_name_data: Name of the MongoDB collection containing the profiles
    :param collection_name_result: Name of the MongoDB collection to save the results to
    :param skip: Number of profiles to skip
    :param limit: Maximum number of profiles to process
    :param experience_prompt: System prompt for experiences
    :param education_prompt: System prompt for education
    :param database: Name of the MongoDB database
    """
    df = load_profiles(client, collection_name_data, skip, limit, database)
    logging.info(f"Loaded {len(df)} profiles (batch starting at {skip})")

    df = preprocess_data(df, experience_prompt, education_prompt)
    df = generate_attributes(df)
    df = postprocess_data(df)

    save_results(client, collection_name_result, df, database)
    logging.info(f"Batch processed and saved (profiles {skip} to {skip + len(df) - 1})")


# Main function
if __name__ == "__main__":
    load_dotenv(find_dotenv())
    log = configure_custom_logger(module_name=__name__)
    log.info("Environment variables loaded, logger initialized.")

    # Connect to MongoDB
    log.info("Connecting to MongoDB...")
    mongodb_client = pymongo.MongoClient(os.getenv('MONGO_CLIENT_URI'))

    # Define constants
    collection_name = os.getenv('MONGO_COLLECTION_NAME')
    database_name = os.getenv('MONGO_DATABASE_NAME')
    batch_size = os.getenv('BATCH_SIZE')

    try:
        # Get total number of profiles
        total_profiles = get_total_profile_count(mongodb_client, collection_name, database_name)
        log.info(f"Total profiles to process: {total_profiles}")

        # Process profiles in batches
        for skip in range(0, total_profiles, batch_size):
            process_batch(
                client=mongodb_client,
                collection_name_data=collection_name,
                collection_name_result=collection_name + "_processed",
                skip=skip,
                limit=batch_size,
                database=database_name
            )

        log.info("All batches processed successfully")

    finally:
        # Close MongoDB connection
        log.info("Closing MongoDB connection...")
        mongodb_client.close()
        log.info("MongoDB connection closed, finished execution.")
