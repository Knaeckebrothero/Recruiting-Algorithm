"""
This module contains functions to preprocess the data for the tagging pipeline.
"""
import json
import re
import pandas as pd
from typing import List, Dict, Any


def _clean_text(text: str) -> str | None:
    if text is None:
        return None
    # Remove extra whitespace and standardize newlines
    return re.sub(r'\s+', ' ', text.strip())


def _process_entry(entry: Dict[str, Any], prompt: str, attributes: List[str]) -> Dict[str, Any]:
    cleaned_entry = {attr: _clean_text(entry.get(attr)) for attr in attributes}

    # Create the message list for the model
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": json.dumps(cleaned_entry)}
    ]

    return {"original": cleaned_entry, "messages": messages}


def _process_experiences(experiences: List[Dict[str, Any]], prompt: str) -> List[Dict[str, Any]]:
    exp_attributes = ['company', 'title', 'description', 'location']
    return [_process_entry(exp, prompt, exp_attributes) for exp in experiences]


def _process_education(education: List[Dict[str, Any]], prompt: str) -> List[Dict[str, Any]]:
    edu_attributes = ['field_of_study', 'degree_name', 'school', 'description']
    return [_process_entry(edu, prompt, edu_attributes) for edu in education]


def preprocess_data(df: pd.DataFrame, experience_prompt: str, education_prompt: str) -> pd.DataFrame:
    print("Preprocessing data...")

    # Process experiences and education for each profile
    df['processed_experiences'] = df['experiences'].apply(_process_experiences(prompt=experience_prompt))
    df['processed_education'] = df['education'].apply(_process_education(prompt=education_prompt))

    return df
