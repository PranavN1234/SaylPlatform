import spacy
from gliner_spacy.pipeline import GlinerSpacy

# Load spaCy model and add GLinER pipeline for product extraction
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("gliner_spacy", config={"labels": ["product_name", "country"]})  # Adding country label

def extract_product_gliner(user_query):
    """
    Extracts product information from the user query using SpaCy, GLinER, and dependency parsing.
    
    Args:
        user_query (str): The query from the user.
        
    Returns:
        str: A concatenated string of the extracted product, country, and packaging (if applicable).
    """
    doc = nlp(user_query)
    extracted_values = []

    # Try extracting using GLinER's 'product_name' label
    for ent in doc.ents:
        if ent.label_ == "product_name" and ent.text.lower() != 'hts':
            extracted_values.append(ent.text)

    # Extract country (GPE or country from GLinER) if mentioned
    for ent in doc.ents:
        if ent.label_ in {"GPE", "country"}:
            extracted_values.append(ent.text)

    # Extract quantity or packaging information (custom rule using dependency parsing)
    for token in doc:
        if token.dep_ in {"nummod", "quantmod"} and token.head.pos_ == "NOUN":
            packaging = f"{token.text} {token.head.text}"
            extracted_values.append(packaging)

    # Fallback to spaCy's NER with 'PRODUCT' label if no product was extracted
    if not extracted_values:
        for ent in doc.ents:
            if ent.label_ == "PRODUCT" and ent.text.lower() != 'hts':
                extracted_values.append(ent.text)

    # Fallback to noun chunk extraction if no product was found
    if not extracted_values:
        common_terms = {'information', 'details', 'documents', 'code', 'codes', 'ruling', 'rulings', 'hts'}
        for chunk in doc.noun_chunks:
            if any(token.pos_ == 'PRON' for token in chunk):
                continue
            if any(token.lemma_.lower() in common_terms for token in chunk):
                continue
            extracted_values.append(chunk.text.strip())
            break

    # Join extracted values with spaces to form a product description
    return ' '.join(extracted_values)
