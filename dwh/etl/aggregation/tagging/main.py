import os
import pymongo
import pandas as pd
import re
import json
from bson import ObjectId
from dotenv import load_dotenv
from typing import List, Dict, Any


def connect_to_mongodb():
    client = pymongo.MongoClient(os.getenv("MONGO_CLIENT_URI"))
    return client


def get_total_profile_count(mongo_client, mongo_collection_name):
    db = mongo_client['raw_data']
    collection = db[mongo_collection_name]

    query = {
        "$or": [
            {"experiences": {"$exists": True, "$ne": []}},
            {"education": {"$exists": True, "$ne": []}}
        ]
    }

    return collection.count_documents(query)


def load_profiles(mongo_client, mongo_collection_name, skip, limit):
    db = mongo_client['raw_data']
    collection = db[mongo_collection_name]

    query = {
        "$or": [
            {"experiences": {"$exists": True, "$ne": []}},
            {"education": {"$exists": True, "$ne": []}}
        ]
    }

    projection = {
        "_id": 1,
        "experiences": 1,
        "education": 1
    }

    profiles = list(collection.find(query, projection).skip(skip).limit(limit))
    return pd.DataFrame(profiles)


def preprocess_data(df: pd.DataFrame, experience_prompt: str, education_prompt: str) -> pd.DataFrame:
    print("Preprocessing data...")

    def clean_text(text: str) -> str:
        if text is None:
            return None
        # Remove extra whitespace and standardize newlines
        return re.sub(r'\s+', ' ', text.strip())

    def process_entry(entry: Dict[str, Any], prompt: str, attributes: List[str]) -> Dict[str, Any]:
        cleaned_entry = {attr: clean_text(entry.get(attr)) for attr in attributes}

        # Create the message list for the model
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(cleaned_entry)}
        ]

        return {"original": cleaned_entry, "messages": messages}

    def process_experiences(experiences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        exp_attributes = ['company', 'title', 'description', 'location']
        return [process_entry(exp, experience_prompt, exp_attributes) for exp in experiences]

    def process_education(education: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        edu_attributes = ['field_of_study', 'degree_name', 'school', 'description']
        return [process_entry(edu, education_prompt, edu_attributes) for edu in education]

    # Process experiences and education for each profile
    df['processed_experiences'] = df['experiences'].apply(process_experiences)
    df['processed_education'] = df['education'].apply(process_education)

    return df


def generate_attributes(df):
    # TODO: Implement attribute generation logic
    print("Generating attributes...")
    return df


def postprocess_data(df):
    # TODO: Implement postprocessing logic
    print("Postprocessing data...")
    return df


def save_results(client, mongo_collection_name, df):
    db = client['processed_data']
    collection = db[mongo_collection_name]

    results = df.to_dict('records')
    for result in results:
        # Ensure _id is an ObjectId
        if not isinstance(result['_id'], ObjectId):
            result['_id'] = ObjectId(result['_id'])

        # Insert the document, or update if it already exists
        collection.replace_one({'_id': result['_id']}, result, upsert=True)

    print(f"Saved {len(results)} results to the database.")


def process_batch(client, mongo_collection_name, skip, limit, experience_prompt, education_prompt):
    df = load_profiles(client, mongo_collection_name, skip, limit)
    print(f"Loaded {len(df)} profiles (batch starting at {skip})")

    df = preprocess_data(df, experience_prompt, education_prompt)
    print(df.head())
    print(df.columns)
    df = generate_attributes(df)
    df = postprocess_data(df)

    save_results(client, mongo_collection_name, df)
    print(f"Batch processed and saved (profiles {skip} to {skip + len(df) - 1})")


def main():
    # Load environment variables
    load_dotenv()

    # Connect to MongoDB
    client = connect_to_mongodb()

    # Define constants
    mongo_collection_name = 'KGL_LIN_PRF_USA'
    batch_size = 100

    # Load prompts
    with open("prompts.json") as f:
        prompts = json.load(f)
        experience_prompt = prompts["experience"]
        education_prompt = prompts["education"]

    try:
        total_profiles = get_total_profile_count(client, mongo_collection_name)
        print(f"Total profiles to process: {total_profiles}")

        for skip in range(0, total_profiles, batch_size):
            process_batch(
                client,
                mongo_collection_name,
                skip,
                batch_size,
                experience_prompt,
                education_prompt
            )

        print("All profiles processed successfully")

    finally:
        client.close()


if __name__ == "__main__":
    main()
