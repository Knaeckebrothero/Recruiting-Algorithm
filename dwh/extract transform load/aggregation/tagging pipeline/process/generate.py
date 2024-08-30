"""
This module contains the functions for generating structured tags.
"""
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
import pandas as pd


class Skill(BaseModel):
    name: str = Field(description="The name of the skill")


class Tag(BaseModel):
    name: str = Field(description="The tag name")


class ExperienceAttributes(BaseModel):
    industry: str = Field(default=None, description="The industry related to the experience")
    profession: str = Field(default=None, description="The profession related to the job title")
    skills: list[Skill] = Field(default=[], description="List of skills relevant to the experience")
    tags: list[Tag] = Field(default=[], description="List of tags relevant to the experience")


def extract_attribute(data, attr):
    # Check if the attribute exists in the data and is not None
    if attr in data and data[attr] is not None:
        if attr in ['skills', 'tags']:
            # Assuming data[attr] is a list of dictionaries with a 'name' key
            try:
                return [item['name'] for item in data[attr]]
            except TypeError:
                # Handles the case where data[attr] might not be a list of dictionaries
                # If it's already a list of names (strings), return as is
                return data[attr]
        else:
            return data[attr]
    return None


def _generate_structured_tags(experience_data: dict[str, str], model, template: str, handler, rate_limiter) -> dict:
    parser = JsonOutputParser(pydantic_object=ExperienceAttributes)
    prompt = PromptTemplate(
        template=template,
        input_variables=["company", "title", "description"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # Wait for the rate limiter
    rate_limiter.wait()

    # Create the chain and make the call
    chain = prompt | model | parser
    result = chain.invoke(experience_data)  # , config={'callbacks': [handler]}

    return result


def apply_tag_generation_to_dataframe(df: pd.DataFrame, model, template: str, callback_handler,
                                      rate_limiter) -> pd.DataFrame:
    """
    Applies the _generate_structured_tags function to each row of the dataframe and adds the generated attributes
    to the existing dataframe.

    :param df: Input DataFrame
    :param model: The model to use for generating tags
    :param template: The template to use for generating tags
    :param callback_handler: The callback handler to use for detailed information
    :param rate_limiter: The rate limiter to use for controlling the rate of requests
    :return: DataFrame with added columns for generated attributes
    """
    def update_row(row, model, template, callback_handler, rate_limiter):
        result = _generate_structured_tags({
            "company": row['company'],
            "title": row['title'],
            "description": row['description']},
            model,
            template,
            callback_handler,
            rate_limiter)
        row['industry'] = extract_attribute(result, 'industry')
        row['profession'] = extract_attribute(result, 'profession')
        row['skills'] = extract_attribute(result, 'skills')
        row['tags'] = extract_attribute(result, 'tags')
        return row

    # Apply the update function to each row
    return df.apply(lambda row: update_row(row, model, template, callback_handler, rate_limiter), axis=1)
