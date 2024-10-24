from .intent_router import route_task
from .product_extractor import extract_product_gliner  # Import product extractor
from .hts_service import find_similar_hts_codes  # Import the HTS similarity function
from .cross_service import find_similar_cross_rulings  # Import the cross rulings similarity function

def handle_user_query(user_query):
    """
    Handle the user query by determining the intent and extracting product information.
    
    Args:
        user_query (str): The query from the user.
        
    Returns:
        dict: Contains the detected intent and product (if applicable).
    """
    intent = route_task(user_query)
    print(f"Detected intent: {intent}")

    response = {"intent": intent}

    if intent in ["hts_inquiry", "cross_rulings_inquiry"]:
        product = extract_product_gliner(user_query)
        if product:
            
            response["product"] = product
            if intent == "hts_inquiry":
                
                # Fetch 10 most similar HTS codes based on product description
                similar_hts = find_similar_hts_codes(product)
                response["similar_hts_codes"] = similar_hts  # Add the similar HTS codes to the response
            elif intent == "cross_rulings_inquiry":
                
                # Fetch 10 most similar cross rulings based on product description
                similar_cross_rulings = find_similar_cross_rulings(product)
                response["similar_cross_rulings"] = similar_cross_rulings  # Add the similar cross rulings to the response
        else:
            
            response["error"] = "No product extracted"
    else:
        print("Handling as a general query.")
        # Handle general queries here

    return response
