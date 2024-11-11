from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from .data_models import BillOfLadingData
from .BOL_models import BOLData
from .image_processing import get_base64_image
from typing import Optional
import json
import logging
import openai
import os

def extract_data_from_base64_images(base64_images) -> BillOfLadingData:
    """Extracts data from the provided base64 images using OpenAI's GPT-4 model."""
    parser = JsonOutputParser(pydantic_object=BillOfLadingData)
    format_response_parser = parser.get_format_instructions()

    prompt_template = '''Extract the following information from the image documents I provide, use a value from the image if you can't make out clearly don't leave anything blank: {format_instructions}'''

    prompt = PromptTemplate(
        template=prompt_template,
        partial_variables={"format_instructions": format_response_parser}
    )

    formatted_prompt = prompt.format()

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": formatted_prompt
                }
            ]
        }
    ]

    for base64_image in base64_images:
        messages[0]["content"].append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        )

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    print(OPENAI_API_KEY)
    openai.api_key = OPENAI_API_KEY

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.0,
    )
    logging.info(f"response is: {response}")
    output = response.choices[0].message.content
    parsed_output = parser.parse(output)

    return BillOfLadingData.parse_obj(parsed_output)


def extract_raw_text_from_gpt(ocr_text: str, system_message: str, prompt: str) -> Optional[str]:
    """
    First API call to GPT-4o to extract data as plain text.

    Parameters:
    - ocr_text (str): The extracted text from OCR.
    - system_message (str): Instruction for the system role.
    - prompt (str): Specific prompt guiding the data extraction.

    Returns:
    - Optional[str]: Raw text data if extraction is successful, or None if there was an error.
    """
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{prompt}\n\nText to extract from:\n{ocr_text}"}
    ]

    try:
        # API call to GPT-4o
        completion = openai.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=messages
        )

        # Access the response content directly
        response_text = completion.choices[0].message.content
        return response_text

    except Exception as e:
        print(f"Error in API call: {e}")
        return None
    
def refine_text_to_boldata(raw_text: str, system_message: str) -> Optional[BOLData]:
    """
    Second API call to GPT-4o to refine extracted text data to match the BOLData structure using Pydantic.

    Parameters:
    - raw_text (str): The initial text data extracted in the first step.
    - system_message (str): Instruction for the system role.

    Returns:
    - Optional[BOLData]: Refined data structured to match BOLData, or None if there was an error.
    """
    # Assume BOLData is the Pydantic model you defined
    response_format = BOLData

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Refine the following data to match the Bill of Lading structure:\n\n{raw_text}"}
    ]

    try:
        # Second call to GPT-4o to refine text to match BOLData structure
        completion = openai.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=messages,
            response_format=response_format
        )

        # Retrieve parsed response directly into BOLData format
        refined_data = completion.choices[0].message.parsed
        return refined_data

    except Exception as e:
        print(f"Error in API call: {e}")
        return None