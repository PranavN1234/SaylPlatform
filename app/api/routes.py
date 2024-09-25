import os
import logging
from flask import request, jsonify, send_file
from app.api import api_blueprint
from app.services.ai_service import extract_data_from_base64_images
from app.services.pdf_service import fill_pdf
from app.utils.field_mapping import field_mapping
from app.services.pdf_service import convert_pdfs_to_images
from app.services.chatbot.handler import handle_user_query
from app.services.chatbot.chatbot_ai import ChatbotAI

import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../data/forms')
INPUT_PDF_PATH = os.path.join(DATA_DIR, 'ISF_FORM.pdf')

@api_blueprint.route('/', methods=['GET'])
def hello_world():
    return jsonify({"version": "apiv2"})

@api_blueprint.route('/process-pdfs', methods=['POST'])
def process_pdfs():
    if 'pdfs' not in request.files:
        return jsonify({"error": "No PDFs provided"}), 400

    pdf_files = request.files.getlist('pdfs')
    base64_images = convert_pdfs_to_images(pdf_files)
    logging.info("Images received!!")	

    # Extract data using AI service
    data = extract_data_from_base64_images(base64_images)
    logging.info("Data extracted!!")	
    # Fill the PDF with extracted data
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as output_pdf_file:
        output_pdf_path = output_pdf_file.name

    fill_pdf(INPUT_PDF_PATH, output_pdf_path, data, field_mapping)
    print("Pdf filled successfully!!!, sending to backend")
    return send_file(output_pdf_path, as_attachment=True, download_name='filled_form.pdf')

chatbot_ai = ChatbotAI()

@api_blueprint.route('/chatbot/query', methods=['POST'])
def chatbot_query():
    try:
        # Get the user query from the request payload
        user_query = request.json.get("query")
        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        # Call the chatbot handler to process the query
        response = handle_user_query(user_query)
        intent = response.get("intent")
        print(response)

        # Generate AI response based on the intent and context
        ai_response = chatbot_ai.generate_gpt_response(intent, response, user_query)

        # Add intent and Search URL to the AI response dictionary
        ai_response_dict = ai_response.dict()
        ai_response_dict['intent'] = intent
        return jsonify(ai_response_dict), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



    
