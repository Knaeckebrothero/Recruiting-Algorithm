"""
This module contains the pydantic models for the tagging pipeline.
"""
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List


class ExperienceTag(BaseModel):
    tag: str = Field(description="The tag name")
    description: str = Field(description="A brief description of what this tag represents")


class ExperienceTags(BaseModel):
    tags: List[ExperienceTag] = Field(description="List of tags for the experience")
