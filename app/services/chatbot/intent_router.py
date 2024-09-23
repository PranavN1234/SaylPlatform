import os
import semantic_router
from dotenv import load_dotenv
from semantic_router.encoders import OpenAIEncoder
from semantic_router import RouteLayer
from semantic_router import Route

def setup_route_layer():
    # Load the .env file
    
    load_dotenv()
    print(semantic_router.__file__)
    # Set the OpenAI API key
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    # Initialize the encoder
    encoder = OpenAIEncoder()

    hts_inquiry = Route(
        name="hts_inquiry",
        utterances=[
            "What is the HTS code for steel pipes?",
            "I need HTS information on cotton fabrics.",
            "Find the Harmonized Tariff Schedule for leather goods.",
            "Can you provide the HTS details for aluminum foil?",
            "What's the tariff code for electronic devices?",
            "I want to look up HTS codes for imported cars.",
            "How do I find HTS information for agricultural products?",
            "Give me the HTS code for plastic containers.",
            "I need the Harmonized Tariff Schedule number for wool.",
            "Can you help me find HTS codes?",
        ],
    )


    cross_rulings_inquiry = Route(
        name="cross_rulings_inquiry",
        utterances=[
            "I need the cross ruling for roma tomatoes.",
            "Can you find the cross rulings related to electronic gadgets?",
            "Show me the cross ruling documents for imported furniture.",
            "Lookup cross rulings on textile imports.",
            "Find me cross rulings about chemical products.",
            "I want to see cross rulings for solar panels.",
            "Provide cross ruling information on footwear.",
            "Get me cross rulings related to automotive parts.",
            "Search for cross rulings on dairy products.",
            "Do you have cross rulings for medical equipment?",
        ],
    )

    general_query = Route(
        name="general_query",
        utterances=[
            "What's the weather today?",
            "Tell me a joke.",
            "How do I reset my password?",
            "What's your favorite movie?",
            "How are you doing?",
            "I need help with my account.",
            "Can you explain the return policy?",
            "Where is the nearest store?",
            "What are your hours of operation?",
            "I want to know about your services.",
            "How can I contact customer support?",
            "Give me information about your company.",
            "I need assistance with an order.",
            "Tell me about the latest news.",
            "How do I subscribe to the newsletter?",
        ],
    )
    # Place all routes into a single list
    routes = [
        hts_inquiry,
        cross_rulings_inquiry,
        general_query
    ]


    # Initialize and return the RouteLayer
    return RouteLayer(encoder=encoder, routes=routes)


rl = setup_route_layer()

def route_task(user_query):
    """
    Routes the user query to the appropriate task.

    Args:
    - user_query (str): The query from the user.

    Returns:
    - str: The name of the route (task) that the query is routed to.
    """
    route = rl(user_query)
    return route.name
