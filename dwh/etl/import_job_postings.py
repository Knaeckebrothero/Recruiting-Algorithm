import os
import dotenv
from pymongo import MongoClient
import json

# Load environment variables
dotenv.load_dotenv(dotenv.find_dotenv())

# MongoDB setup
client = MongoClient(os.getenv("MongoClientURI"))
mongodb = client['raw_data']
collection = mongodb['KGL_JPS']

# File and sampling setup

filename = 'techmap-jobs-dump-2021-09.json'
total_lines = 3470024
desired_samples = 35000
my_script_counter = 0
interval = total_lines // desired_samples

# Sampling and loading data
with open(filename, 'r', encoding='utf-8') as file:
    selected_objects = []
    for i, line in enumerate(file):
        # Print progress
        my_script_counter += 1
        print(f"Progress: {my_script_counter}")

        # Insert in batches to manage memory usage
        if i % interval == 0:
            try:
                json_data = json.loads(line.strip())
                # Rename the '_id' field to 'original_id'
                if '_id' in json_data:
                    json_data['original_id'] = json_data.pop('_id')
                selected_objects.append(json_data)
                # Insert in batches to manage memory usage
                if len(selected_objects) >= 1000:
                    collection.insert_many(selected_objects)
                    selected_objects = []
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line {i}: {e}")

    # Insert any remaining documents in the batch
    if selected_objects:
        collection.insert_many(selected_objects)

print("Data loading complete.")
