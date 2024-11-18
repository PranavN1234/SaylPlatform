field_mapping = {
    # General Information
    "reference_number": "Reference #",
    "contact_name": "Contact Name",
    "contact_phone": "Contact Phone",

    # Principal Party Information
    "principle_party_name": "PRINCIPLE PARTY IN INTEREST Name",
    "principle_party_ein": "PRINCIPLE PARTY IN INTEREST EIN",
    "principle_party_address": "PRINCIPLE PARTY IN INTEREST Address/Cargo Location",
    "principle_party_state_of_origin": "PRINCIPLE PARTY IN INTEREST State of Origin",

    # Ultimate Consignee Information
    "ultimate_consignee_type": "ULTIMATE CONSIGNEE Consignee Type",
    "ultimate_consignee_name_address": "ULTIMATE CONSIGNEE Name/Address",
    "ultimate_consignee_country_destination": "ULTIMATE CONSIGNEE Country of Ultimate Destination",
    "ultimate_consignee_fppi_name": "ULTIMATE CONSIGNEE FPPI Name",

    # Conditional Fields
    "related_parties": {
        True: "Related Parties YES",
        False: "Related Parties NO"
    },
    "routed_export_transaction": {
        True: "Routed Export Transaction YES",
        False: "Routed Export Transaction NO"
    },
    "hazardous_materials": {
        True: "Hazardous Materials YES",
        False: "Hazardous Materials NO"
    },
    "ftz_identifier": "OTHER CONDITIONAL FTZ Identifier",
    "intermediate_consignee": "OTHER CONDITIONAL Intermediate Consignee Name & Address",
    "entry_number": "OTHER CONDITIONAL Entry #",

    # Transportation Information
    "method_of_transportation": {
        "Air": "Method of Transportation-Air",
        "Ocean": "Method of Transportation-Ocean",
        "Truck": "Method of Transportation-Truck",
        "Rail": "Method of Transportation-Rail"
    },
    "port_of_export": "Port of Export",
    "port_of_unlading": "Port of Unlading",
    "vessel_name": "Vessel Name",
    "date_of_export": "Date of Export",

    # Charges
    "charges_freight": {
        "Prepaid": "Charges - Freight - Prepaid",
        "Collect": "Charges - Freight - Collect"
    },
    "charges_duty": {
        "Prepaid": "Charges - Duty - Prepaid",
        "Collect": "Charges - Duty - Collect"
    },
    "charges_tax": {
        "Prepaid": "Charges - Tax - Prepaid",
        "Collect": "Charges - Tax - Collect"
    },
    "charges_customs": {
        "Prepaid": "Charges - Customs - Prepaid",
        "Collect": "Charges - Customs - Collect"
    },

    # Insurance
    "insurance_requested": {
        True: "Insurance Requested - Yes",
        False: "Insurance Requested - No"
    },
    "amount_of_insurance": "Amount of Insurance",
    "declared_value_for_carriage": "Declared Value for Carriage",

    # Items Details
    "items": {
        "origin": "Origin",
        "commodity_description": "Commodity Description",
        "schedule_b_or_hts": "Schedule B or HTS",
        "eccn_or_usml_category": "ECCN or USML Category",
        "quantity_top": "Quantity Top",
        "uom_top": "UOM Top",
        "gross_weight": "Gross Weight",
        "gross_weight_dropdown": "gross weight dropdown",
        "export_value": "Export Value",
        "license_or_cfr": "Lic# / CFR",
        "sme": {
            True: "SME",
            False: None
        },
        "ddtc_qty_uom": "DDTC Qty/UOM",
        "quantity_bottom": "Quantity Bottom",
        "uom_bottom": "UOM Bottom",
        "license_value": "License Value",
    },

    # Signature
    "title": "Title",
    "signature_date": "Signature - Date"
}

def generate_sli_mapped_data(json_data):
    """
    Generates mapped_data dictionary for filling PDF form fields based on JSON data.

    Parameters:
    - json_data (dict): JSON data containing values to populate in the PDF.

    Returns:
    - dict: Mapped data ready to be used for PDF form filling.
    """
    mapped_data = {}

    # General fields
    for json_key, pdf_field in field_mapping.items():
        if json_key in json_data:
            value = json_data[json_key]

            if isinstance(pdf_field, str):  # Direct mapping
                mapped_data[pdf_field] = value if value is not None else ""
            elif isinstance(pdf_field, dict):  # Conditional mappings (e.g., boolean fields)
                if isinstance(value, (bool, str)) and value in pdf_field:  # Ensure value is hashable
                    mapped_data[pdf_field[value]] = True

    # Item details with indexed fields
    if "items" in json_data and isinstance(json_data["items"], list):  # Handling "items" as a list
        for idx, item in enumerate(json_data["items"], start=1):
            for item_key, pdf_field_base in field_mapping["items"].items():
                if item_key in item:
                    item_value = item[item_key]

                    if isinstance(pdf_field_base, dict):  # For conditional fields like SME
                        if item_value in pdf_field_base:
                            field_name = f"{idx}-{pdf_field_base[item_value]}"  # Correctly format field name
                            mapped_data[field_name] = True
                    else:  # Regular fields
                        field_name = f"{idx}-{pdf_field_base}"  # Format as number-name
                        mapped_data[field_name] = item_value if item_value is not None else ""

    return mapped_data

