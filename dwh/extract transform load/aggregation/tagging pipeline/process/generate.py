"""
This module contains the functions for generating structured tags.
"""
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
import pandas as pd
import json


class ExperienceTag(BaseModel):
    tag: str = Field(description="The tag name")
    description: str = Field(description="A brief description of what this tag represents")


class ExperienceTags(BaseModel):
    tags: list[ExperienceTag] = Field(description="List of tags for the experience")


def _generate_structured_tags(experience_data: dict[str, str], model, template: str) -> dict:
    parser = JsonOutputParser(pydantic_object=ExperienceTags)
    prompt = PromptTemplate(
        template=template,
        input_variables=["company", "title", "description"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    chain = prompt | model | parser
    result = chain.invoke(experience_data)

    return result


def _process_dataframe_row(row, model, template: str) -> dict:
    return _generate_structured_tags({
        "company": row['company'],
        "title": row['title'],
        "description": row['description']},
        model,
        template
    )


def apply_tag_generation_to_dataframe(df: pd.DataFrame, model, template: str) -> pd.DataFrame:
    """
    Applies the process_dataframe_row function to each row of the dataframe and adds the generated attributes
    to the existing dataframe.

    :param df: Input DataFrame
    :param model: The model to use for generating tags
    :param template: The template to use for generating tags
    :return: DataFrame with added columns for generated tags
    """
    # Apply the process_dataframe_row function to each row
    generated_tags = df.apply(lambda row: _process_dataframe_row(row, model, template), axis=1)

    # Function to extract specific attributes from the generated tags
    def extract_attribute(tags, attr):
        return [tag[attr] for tag in tags['tags']]

    # Add new columns to the dataframe
    df['generated_tags'] = generated_tags.apply(lambda x: json.dumps(x['tags']))
    df['tag_names'] = generated_tags.apply(lambda x: extract_attribute(x, 'tag'))
    df['tag_descriptions'] = generated_tags.apply(lambda x: extract_attribute(x, 'description'))

    return df
