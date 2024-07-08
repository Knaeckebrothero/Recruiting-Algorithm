"""
This module contains functions to generate attributes for the tagging pipeline.
"""
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import List, Dict, Any

"""
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
"""


def generate_attributes(df: pd.DataFrame) -> pd.DataFrame:
    # Set system prompt
    messages = [{
        "role": "system",
        "content": },
        {
            "role": "user",
            "content": "Context: " + context + "\n\nTemplate: " + json.dumps(template)}]

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
