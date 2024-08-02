import os
from flask import request, jsonify, send_file
from app.api import api_blueprint
from app.services.ai_service import extract_data_from_base64_images
from app.services.pdf_service import fill_pdf
from app.utils.field_mapping import field_mapping
import base64
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../data/forms')
INPUT_PDF_PATH = os.path.join(DATA_DIR, 'ISF_FORM.pdf')

@api_blueprint.route('/', methods=['GET'])
def hello_world():
    return jsonify({"hello world": "hello world"})

@api_blueprint.route('/process-images', methods=['POST'])
def process_images():
    if 'images' not in request.files:
        return jsonify({"error": "No images provided"}), 400

    image_files = request.files.getlist('images')
    base64_images = []

    for image_file in image_files:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        base64_images.append(base64_image)

    # Extract data using AI service
    data = extract_data_from_base64_images(base64_images)

    # Fill the PDF with extracted data
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as output_pdf_file:
        output_pdf_path = output_pdf_file.name

    fill_pdf(INPUT_PDF_PATH, output_pdf_path, data, field_mapping)
    print("Pdf filled successfully!!!, sending to backend")
    return send_file(output_pdf_path, as_attachment=True, download_name='filled_form.pdf')
