"""
This script holds the main function for the tagging pipeline.
"""
import os
import pymongo
import pandas as pd
from dotenv import load_dotenv, find_dotenv
# from bson import ObjectId
from langchain_openai import ChatOpenAI
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from collections import deque
import time
from multiprocessing import Pool, cpu_count
from functools import partial

from custom_logger import configure_custom_logger
from preprocess import clean_text
from process.generate import apply_tag_generation_to_dataframe


class RateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.request_times = deque()

    def wait(self):
        current_time = time.time()

        # Remove old requests
        while self.request_times and current_time - self.request_times[0] > self.time_window:
            self.request_times.popleft()

        # If we've reached the limit, wait
        if len(self.request_times) >= self.max_requests:
            sleep_time = self.time_window - (current_time - self.request_times[0])
            if sleep_time > 0:
                time.sleep(sleep_time)

        # Add the current request
        self.request_times.append(time.time())


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


def process_batch(start, batch_size, total_profiles, model_name, template,
                  mongodb_uri, database_name, collection_name, result_collection_name, query, projection):
    log = configure_custom_logger(
        module_name=__name__,
        logging_directory=os.getenv('LOGGING_DIRECTORY'),
        console_level=10
    )
    # Connect to MongoDB within the process
    mongodb_client = pymongo.MongoClient(mongodb_uri)

    # Create a new RateLimiter instance for this process
    rate_limiter = RateLimiter(max_requests=70, time_window=61)

    # Create a new ChatOpenAI instance for this process
    model = ChatOpenAI(
        model=model_name,
        temperature=0,
        seed=42,
        n=1,
    )

    # Create a new DetailedCallbackHandler instance for this process
    handler = DetailedCallbackHandler()

    # Load profiles
    df = load_profiles(
        mongodb_client, collection_name, start, batch_size, database_name, query, projection)
    log.info(f"Loaded {len(df)} profiles (batch starting at {start})")

    # Clean the text in the DataFrame
    df = df.map(clean_text)

    # Apply the preprocessing function
    df = apply_tag_generation_to_dataframe(df, model, template, handler, rate_limiter)

    # Save the results to MongoDB
    save_results(mongodb_client, result_collection_name, df, database_name)
    log.info(f"Batch processed and saved (profiles {start} to {start + len(df) - 1})")

    # Close MongoDB connection
    mongodb_client.close()

    return len(df)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    log = configure_custom_logger(
        module_name=__name__,
        logging_directory=os.getenv('LOGGING_DIRECTORY'),
        console_level=10
    )
    log.info("Environment variables loaded, logger initialized.")

    # Connect to MongoDB
    log.info("Connecting to MongoDB...")
    mongodb_client = pymongo.MongoClient(os.getenv('MONGO_CLIENT_URI'))

    # Define constants
    database_name = os.getenv('MONGO_DATABASE_NAME')
    collection_name = os.getenv('MONGO_COLLECTION_NAME')
    result_collection_name = os.getenv('MONGO_COLLECTION_NAME_RESULT')
    batch_size = int(os.getenv('BATCH_SIZE'))
    model_name = os.getenv('MODEL_NAME')

    with open("prompt.txt", "r") as f:
        template = f.read()

    # Query to filter profiles with non-empty descriptions
    query = {
        "description": {"$nin": [None, ""]}
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

        # Determine the number of processes to use
        # Use up to 8 processes or the number of CPU cores, whichever is smaller
        num_processes = min(cpu_count(), 4)
        log.info(f"Using {num_processes} processes to process profiles")

        # Create a pool of worker processes
        with Pool(num_processes) as pool:
            # Prepare the partial function with fixed arguments
            process_batch_partial = partial(
                process_batch,
                total_profiles=total_profiles,
                model_name=model_name,
                template=template,
                mongodb_uri=os.getenv('MONGO_CLIENT_URI'),
                database_name=database_name,
                collection_name=collection_name,
                result_collection_name=result_collection_name,
                query=query,
                projection=projection
            )

            # Process profiles in parallel
            results = pool.starmap(process_batch_partial, [(i, batch_size) for i in range(0, total_profiles, batch_size)])

        # Log when all batches are processed
        log.info(f"All batches processed successfully. Total profiles processed: {sum(results)}")

    finally:
        # Close MongoDB connection
        log.info("Closing MongoDB connection...")
        mongodb_client.close()
        log.info("MongoDB connection closed, finished execution.")
