"""
This module contains the postprocessing logic for the tagging pipeline.
"""


def postprocess_data(df):
    # TODO: Implement postprocessing logic
    print("Postprocessing data...")
    return df




import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import List, Dict, Any



def generate_attributes(df: pd.DataFrame, model_path: str, batch_size: int = 4) -> pd.DataFrame:
    print("Generating attributes...")

    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16, device_map="auto")

    def process_batch(batch: List[Dict[str, Any]]) -> List[str]:
        # Tokenize and pad the inputs
        inputs = [item['messages'] for item in batch]
        tokenized_inputs = tokenizer(inputs, padding=True, truncation=True, return_tensors="pt").to(model.device)

        # Generate outputs
        with torch.no_grad():
            outputs = model.generate(
                **tokenized_inputs,
                max_new_tokens=150,  # Adjust as needed
                do_sample=True,
                temperature=0.7,
                num_return_sequences=1
            )

        # Decode outputs
        decoded_outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return decoded_outputs

    def process_experiences(experiences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for i in range(0, len(experiences), batch_size):
            batch = experiences[i:i + batch_size]
            outputs = process_batch(batch)
            for exp, output in zip(batch, outputs):
                results.append({**exp['original'], 'generated_attributes': output})
        return results

    # Process experiences and education
    df['processed_experiences'] = df['processed_experiences'].apply(process_experiences)
    df['processed_education'] = df['processed_education'].apply(process_experiences)

    return df



def generate_attributes(df: pd.DataFrame) -> pd.DataFrame:


    # Generate a completion
    example_completion = openai_api_client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages,
        temperature=0.9




    def process_batch(batch: List[Dict[str, Any]]) -> List[str]:
        # Tokenize and pad the inputs
        inputs = [item['messages'] for item in batch]
        tokenized_inputs = tokenizer(inputs, padding=True, truncation=True, return_tensors="pt").to(model.device)

        # Generate outputs
        with torch.no_grad():
            outputs = model.generate(
                **tokenized_inputs,
                max_new_tokens=150,  # Adjust as needed
                do_sample=True,
                temperature=0.7,
                num_return_sequences=1
            )

        # Decode outputs
        decoded_outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return decoded_outputs

    def process_experiences(experiences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for i in range(0, len(experiences), batch_size):
            batch = experiences[i:i + batch_size]
            outputs = process_batch(batch)
            for exp, output in zip(batch, outputs):
                results.append({**exp['original'], 'generated_attributes': output})
        return results

    # Process experiences and education
    df['processed_experiences'] = df['processed_experiences'].apply(process_experiences)
    df['processed_education'] = df['processed_education'].apply(process_experiences)

    return df

    # Load prompts
    with open("prompts.json") as f:
        prompts = json.load(f)
        experience_prompt = prompts["experience"]
        education_prompt = prompts["education"]


def _process_entry(entry: Dict[str, Any], prompt: str, attributes: List[str]) -> Dict[str, Any]:
    """
    Process an entry by cleaning the text and creating a message list for the model.

    :param entry: Entry to process (e.g. experience, education)
    :param prompt: System prompt for the model
    :param attributes: List of attributes to include in the message list

    :return: Processed entry with original data and message list
    """
    cleaned_entry = {attr: _clean_text(entry.get(attr)) for attr in attributes}

    # Create the message list for the model
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": json.dumps(cleaned_entry)}
    ]

    return {"original": cleaned_entry, "messages": messages}


def _process_experiences(experiences: List[Dict[str, Any]], prompt: str) -> List[Dict[str, Any]]:
    """
    Process experiences for each profile.

    :param experiences:
    :type experiences:
    :param prompt:
    :type prompt:
    :return:
    :rtype:
    """
    exp_attributes = ['company', 'title', 'description', 'location']
    return [_process_entry(exp, prompt, exp_attributes) for exp in experiences]


def _process_education(education: List[Dict[str, Any]], prompt: str) -> List[Dict[str, Any]]:
    edu_attributes = ['field_of_study', 'degree_name', 'school', 'description']
    return [_process_entry(edu, prompt, edu_attributes) for edu in education]

