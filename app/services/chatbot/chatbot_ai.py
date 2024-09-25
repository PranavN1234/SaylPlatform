from openai import OpenAI
from .models import CrossRulingsResponse, HTSResponse, GeneralResponse
from typing import Dict, Union


class ChatbotAI:
    def __init__(self):
        self.openai_client = OpenAI()

    def generate_gpt_response(self, intent: str, context: Dict, user_query: str) -> Union[CrossRulingsResponse, HTSResponse, GeneralResponse]:
        """
        Generates a structured response using OpenAI's GPT model based on the detected intent.

        Args:
            intent (str): The detected intent ('hts_inquiry', 'cross_rulings_inquiry', or 'general_query').
            context (Dict): The context from the respective service (HTS or Cross Rulings).
            user_query (str): The original query from the user.

        Returns:
            Union[CrossRulingsResponse, HTSResponse, GeneralResponse]: The structured response based on the intent.
        """

        # Prepare the system message and user message based on the intent
        system_message = "You are an expert assistant helping with HTS codes and cross rulings inquiries."

        # Format the context for the prompt
        prompt = f"Analyze the following context for the user's query: '{user_query}' and provide the best information:\n\n{context}"

        # Choose the appropriate response format based on the intent
        if intent == "cross_rulings_inquiry":
            response_format = CrossRulingsResponse
        elif intent == "hts_inquiry":
            response_format = HTSResponse
        else:
            # Handle general queries
            response_format = GeneralResponse

        # Call OpenAI with the formatted context and expected response format
        completion = self.openai_client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            response_format=response_format
        )

        # Parse the message and return the appropriate structured response
        message = completion.choices[0].message
        if message.parsed:
            return message.parsed  # Parsed into the correct Pydantic model
        else:
            raise ValueError(f"Failed to parse response: {message.refusal}")
