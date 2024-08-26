"""
This module contains functions to preprocess the data for the tagging pipeline.
"""
import regex


def clean_text(text: str) -> str | None:
    """
    This function cleans the input text by normalizing line breaks,
    removing symbols and pictographs, replacing sequences of whitespace with a single space
    and removes leading and trailing whitespace.
    Before returning the cleaned text.

    :param text: Input text
    :return: Cleaned text
    """
    if isinstance(text, str):
        # Normalize all types of line breaks to a single newline character
        text = regex.sub(r'\r\n|\r|\n', '\n', text)

        # Removes symbols and pictographs while keeping letters, numbers, and common punctuation
        text = regex.sub(r'[\p{So}\p{C}]+', '', text, flags=regex.UNICODE)

        # Replace sequences of whitespace with a single space
        text = regex.sub(r'\s+', ' ', text)

        # Remove leading and trailing whitespace
        text = text.strip()

        return text
    else:
        return None

# TODO: Add a function to calculate the length of the object based on the starts_at and ends_at attributes.
