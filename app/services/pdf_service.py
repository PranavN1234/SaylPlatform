import PyPDF2
from .data_models import BillOfLadingData
from pdf2image import convert_from_path
import tempfile
import base64
import pdfplumber
from typing import List
from werkzeug.datastructures import FileStorage
import fitz

def fill_pdf(input_pdf_path, output_pdf_path, data: BillOfLadingData, field_mapping):
    with open(input_pdf_path, "rb") as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

            # Fill the fields with data
            for key, value in data.dict(exclude_unset=True).items():
                if key in field_mapping:
                    field_name = field_mapping[key]
                    if value is not None:
                        pdf_writer.update_page_form_field_values(pdf_writer.pages[page_num], {field_name: value})

            # Handle items separately
            for i, item in enumerate(data.items[:8], start=1):
                item_desc_key = f"Itemdesc{i}"
                hts_number_key = f"HTSnumber{i}"
                country_origin_key = f"Countryoforigin{i}"

                item_desc_value = item.description
                hts_number_value = item.hts_number
                country_origin_value = item.country_of_origin

                pdf_writer.update_page_form_field_values(pdf_writer.pages[page_num], {
                    item_desc_key: item_desc_value,
                    hts_number_key: hts_number_value,
                    country_origin_key: country_origin_value
                })

        # Write the filled PDF to a new file
        with open(output_pdf_path, "wb") as output_file:
            pdf_writer.write(output_file)

def convert_pdfs_to_images(pdf_files):
    """
    Converts PDF files to images and returns a list of base64 encoded images.
    """
    base64_images = []

    for pdf_file in pdf_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf_file:
            pdf_file.save(temp_pdf_file.name)
            images = convert_from_path(temp_pdf_file.name, poppler_path=r'C:\Program Files\poppler-24.07.0\Library\bin')
            for image in images:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_image_file:
                    image.save(temp_image_file.name, 'PNG')
                    with open(temp_image_file.name, 'rb') as img_file:
                        base64_image = base64.b64encode(img_file.read()).decode('utf-8')
                        base64_images.append(base64_image)

    return base64_images

def extract_text_from_pdfs(pdf_files: List[FileStorage]) -> str:
    """
    Extracts text from multiple PDF files and formats it as "PDF Title" followed by the content.
    Each PDF's content is separated by a line break.

    Parameters:
    pdf_files (List[FileStorage]): List of in-memory FileStorage PDF files from Flask.

    Returns:
    str: Concatenated text with each PDF's title and content.
    """
    text = ''

    for pdf_file in pdf_files:
        pdf_title = pdf_file.filename  # Get the filename directly
        text += f"{pdf_title}\n"  # Add the title

        # Use pdf_file.stream to read the in-memory file
        with pdfplumber.open(pdf_file.stream) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'

        text += '\n'  # Add a blank line after each PDF content

    return text

def fill_pdf_with_pymupdf(template_pdf_path, output_pdf_path, mapped_data):
    """
    Fills form fields in a PDF template with data from `mapped_data` using PyMuPDF.

    Parameters:
    - template_pdf_path (str): Path to the original PDF template with form fields.
    - output_pdf_path (str): Path to save the filled PDF.
    - mapped_data (dict): Dictionary containing field names and values to populate.
    """
    # Open the template PDF
    pdf_document = fitz.open(template_pdf_path)

    # Iterate over each page in the PDF
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]

        # Access the form fields (widgets) on the page
        form_fields = page.widgets()

        if form_fields:
            for field in form_fields:
                field_name = field.field_name
                if field_name and field_name in mapped_data:
                    # Set the field value
                    field.field_value = str(mapped_data[field_name])  # Convert to string if necessary
                    field.update()  # Update the widget to reflect the new value

    # Save the modified PDF
    pdf_document.save(output_pdf_path)
    pdf_document.close()
    print(f"PDF saved as {output_pdf_path}")