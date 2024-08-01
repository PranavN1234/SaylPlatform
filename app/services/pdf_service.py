import PyPDF2
from .data_models import BillOfLadingData

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
