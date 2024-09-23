import requests
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load pre-trained T5 model and tokenizer for text summarization
model_name = "t5-small"  # You can also try t5-base for better quality
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Function to summarize text using T5
def summarize_text(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Function to fetch cross rulings data from the API
def fetch_cross_rulings_data(keyword, max_pages=1):
    api_url = 'https://rulings.cbp.gov/api/search'
    all_rulings = []
    
    for page in range(1, max_pages + 1):
        params = {'term': keyword, 'collection': 'ALL', 'sortBy': 'RELEVANCE', 'pageSize': 30, 'page': page}
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            rulings = data.get('rulings', [])
            all_rulings.extend(rulings)
        else:
            print(f"Failed to fetch data: {response.status_code}")
            break
    return all_rulings

# Function to preprocess text (lowercasing and removing stopwords)
def preprocess(text):
    tokens = text.lower().split()
    return [token for token in tokens if token not in ENGLISH_STOP_WORDS]

# Function to calculate BM25 similarity between descriptions and the target product
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

# Function to fetch detailed ruling information and summarize it
def fetch_ruling_details(ruling_number, search_query):
    api_url = f"https://rulings.cbp.gov/api/ruling/{ruling_number}"
    params = {'textToHighlight': search_query}
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        full_text = data.get('text', 'No full text available.')

        # Summarize the full text
        summary = summarize_text(full_text)

        return {
            'Summary': summary,
            'URL': 'https://rulings.cbp.gov' + data.get('url', ''),
            'ID': data.get('id', 'N/A'),
            'Tariffs': data.get('tariffs', []),
            'Related Rulings': data.get('relatedRulings', [])
        }
    return None

# Main function to find similar cross rulings and return the top N summaries (with failsafe)
def find_similar_cross_rulings(target_product, max_pages=1, max_results=5):
    rulings_data = fetch_cross_rulings_data(target_product, max_pages)
    
    # Check if there are any rulings to process
    if not rulings_data:
        print("No rulings found for the given product.")
        return []

    # Extract descriptions (subjects) from rulings data
    descriptions = [ruling['subject'] for ruling in rulings_data]
    
    if not descriptions:
        print("No descriptions found in the rulings data.")
        return []

    # Calculate similarity scores using BM25
    similar_descriptions = calculate_bm25_similarity(target_product, descriptions)
    
    # Determine the number of records to return (minimum of max_results or available descriptions)
    num_records = min(len(similar_descriptions), max_results)
    
    # Get the top N similar rulings
    top_similar = similar_descriptions[:num_records]
    
    # Fetch detailed information and summaries for the top similar rulings
    top_similar_records = []
    for i, _ in top_similar:
        ruling_number = rulings_data[i]['rulingNumber']
        details = fetch_ruling_details(ruling_number, target_product)
        if details:
            # Include the subject as the title
            details['Title'] = rulings_data[i]['subject']
            top_similar_records.append(details)

    return top_similar_records