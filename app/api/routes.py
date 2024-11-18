import os
import logging
import json
import zipfile
import io
from flask import request, jsonify, send_file
from app.api import api_blueprint
from app.models.user_model import User  # Import the User model
from flask_jwt_extended import jwt_required  # Import JWT protection
from app.services.ai_service import extract_data_from_base64_images, extract_raw_text_from_gpt, refine_text_to_model
from app.services.pdf_service import fill_pdf, fill_pdf_with_pymupdf
from app.utils.field_mapping import field_mapping
from app.services.pdf_service import convert_pdfs_to_images
from app.services.chatbot.handler import handle_user_query
from app.services.chatbot.chatbot_ai import ChatbotAI
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.BOL_mapping import generate_mapped_data
from app.utils.SLI_mapping import generate_sli_mapped_data
from app.models.conversation_model import Conversation, Message
from app.services.BOL_models import BOLData
from app.services.SLI_models import ExpeditorsSLIData
from app.services.pdf_service import extract_text_from_pdfs
from app import db

import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../data/forms')
INPUT_PDF_PATH = os.path.join(DATA_DIR, 'ISF_FORM.pdf')
INPUT_BOL_PATH = os.path.join(DATA_DIR, 'BOL.pdf')
INPUT_SLI_PATH = os.path.join(DATA_DIR, 'SLI.pdf')

@api_blueprint.route('/', methods=['GET'])
def hello_world():
    return jsonify({"version": "apiv5"})


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

@api_blueprint.route('/process-BOL-pdfs', methods=['POST'])
def process_BOL__pdfs():
    if 'pdfs' not in request.files:
        return jsonify({"error": "No PDFs provided"}), 400

    pdf_files = request.files.getlist('pdfs')
    extracted_text = extract_text_from_pdfs(pdf_files)
    logging.info("Text Extracted!")

    # AI service calls
    system_message = "You are an AI assistant that extracts structured data in plain text."
    initial_prompt = "Please interpret and extract relevant information in json format from the following text."

    initial_text = extract_raw_text_from_gpt(extracted_text, system_message, initial_prompt)

    if not initial_text:
        logging.error("Failed to extract initial text data.")
        return jsonify({"error": "Failed to extract initial text data."}), 500

    # Refine to BOL data
    bol_refined_data = refine_text_to_model(initial_text, system_message, BOLData)
    if not bol_refined_data:
        logging.error("Failed to refine text data to match BOL structure.")
        return jsonify({"error": "Failed to refine text data to match BOL structure."}), 500

    # Refine to SLI data
    sli_refined_data = refine_text_to_model(initial_text, system_message, ExpeditorsSLIData)
    if not sli_refined_data:
        logging.error("Failed to refine text data to match SLI structure.")
        return jsonify({"error": "Failed to refine text data to match SLI structure."}), 500

    # Map data to PDF fields
    bol_mapped_data = generate_mapped_data(bol_refined_data.model_dump())
    sli_mapped_data = generate_sli_mapped_data(sli_refined_data.model_dump())

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as bol_output_pdf_file:
        bol_output_pdf_path = bol_output_pdf_file.name

    fill_pdf_with_pymupdf(INPUT_BOL_PATH, bol_output_pdf_path, bol_mapped_data)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as sli_output_pdf_file:
        sli_output_pdf_path = sli_output_pdf_file.name


    fill_pdf_with_pymupdf(INPUT_SLI_PATH, sli_output_pdf_path, sli_mapped_data)

    logging.info("BOL and SLI PDFs filled successfully!")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(bol_output_pdf_path, "filled_BOL_form.pdf")
        zipf.write(sli_output_pdf_path, "filled_SLI_form.pdf")
    zip_buffer.seek(0)

    # Cleanup temporary files
    os.remove(bol_output_pdf_path)
    os.remove(sli_output_pdf_path)

    # Send the ZIP file to the frontend
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='filled_forms.zip'
    )


chatbot_ai = ChatbotAI()

@api_blueprint.route('/chatbot/query', methods=['POST'])
@jwt_required()
def chatbot_query():
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_query = request.json.get("query")
        session_id = request.json.get("session_id")

        if not user_query or not session_id:
            return jsonify({"error": "No query or session_id provided"}), 400

        conversation = Conversation.query.filter_by(session_id=session_id, user_id=user.id).first()
        if not conversation:
            conversation = Conversation(session_id=session_id, user_id=user.id)
            db.session.add(conversation)
            db.session.commit()

        latest_message_batch = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.created_at.desc()).first()

        if not latest_message_batch:
            # Create a new batch with the user message if none exists
            new_message_batch = Message(conversation_id=conversation.id, user_id=user.id, messages=[{"role": "user", "content": user_query}])
            db.session.add(new_message_batch)
            db.session.commit()
            current_messages = new_message_batch.messages
            latest_message_batch = new_message_batch
        else:
            # Ensure the existing batch's messages is a list
            current_messages = latest_message_batch.messages or []
            if isinstance(current_messages, dict):  # If it's a dict, convert to list of dicts
                current_messages = [current_messages]
            current_messages.append({"role": "user", "content": user_query})

        # Check if the current batch has reached the limit
        if len(current_messages) >= 20:
            new_message_batch = Message(conversation_id=conversation.id, user_id=user.id, messages=[{"role": "user", "content": user_query}])
            db.session.add(new_message_batch)
            db.session.commit()
            latest_message_batch = new_message_batch
        else:
            latest_message_batch.messages = current_messages
            db.session.commit()

        response = handle_user_query(user_query)
        intent = response.get("intent")

        ai_response = chatbot_ai.generate_gpt_response(intent, response, user_query)
        ai_response_json = ai_response.model_dump_json()
        ai_response_dict = json.loads(ai_response_json)

        # Add AI response
        current_messages.append({"role": "assistant", "content": ai_response_dict})

        # Handle batch limit for AI response
        if len(current_messages) >= 20:
            new_message_batch = Message(conversation_id=conversation.id, user_id=user.id, messages=[{"role": "assistant", "content": ai_response_dict}])
            db.session.add(new_message_batch)
            db.session.commit()
        else:
            latest_message_batch.messages = current_messages
            db.session.commit()

        return jsonify({
            "intent": intent,
            "ai_response": ai_response_dict
        }), 200

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500










    
