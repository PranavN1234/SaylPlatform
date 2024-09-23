from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from .data_models import BillOfLadingData
from .image_processing import get_base64_image
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
