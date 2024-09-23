import requests
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Function to fetch HTS data from the API
def fetch_hts_data(keyword):
    url = f"https://hts.usitc.gov/reststop/search?keyword={keyword}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return []

# Function to preprocess text (lowercasing and removing stopwords)
def preprocess(text):
    tokens = text.lower().split()
    return [token for token in tokens if token not in ENGLISH_STOP_WORDS]

# Function to calculate BM25 similarity
def calculate_bm25_similarity(target_product, descriptions):
    # Preprocess the product description and all other descriptions
    processed_descriptions = [preprocess(description) for description in descriptions]
    processed_product = preprocess(target_product)
    
    # Initialize the BM25 model
    bm25 = BM25Okapi(processed_descriptions)
    
    # Get similarity scores
    scores = bm25.get_scores(processed_product)
    
    # Sort descriptions by similarity scores (highest first)
    sorted_indices = scores.argsort()[::-1]
    sorted_descriptions = [(i, scores[i]) for i in sorted_indices]
    
    return sorted_descriptions

# Main function to find similar HTS codes and return the full JSON for top 10 similar entries
def find_similar_hts_codes(target_product):
    hts_data = fetch_hts_data(target_product)
    
    # Extract descriptions from HTS data
    descriptions = [item['description'] for item in hts_data if 'description' in item]
    
    if not descriptions:
        print("No descriptions found")
        return []

    # Calculate similarity scores using BM25
    similar_descriptions = calculate_bm25_similarity(target_product, descriptions)
    
    # Get top 10 similar descriptions (full JSON)
    top_similar = similar_descriptions[:10]
    
    # Return the full records corresponding to the top similar descriptions
    top_similar_records = [hts_data[i] for i, _ in top_similar]
    
    return top_similar_records
