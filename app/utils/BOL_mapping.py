field_mapping = {
    # Terms
    "customer_accept_terms": "Customer_Accept_Terms",
    "term_prepaid": "Term_Pre",
    "term_collect": "Term_Collect",

    # Payment and Charges
    "cash_on_delivery": "COD",  # Adjusted to match extracted name
    "percentage": "Per",  # Adjusted to match extracted name
    "amount": "Amt",
    "weight_total": "WT_ttl",  # Adjusted to match extracted name
    "package_quantity_total": "Pkg_QTY_ttl",
    "handling_unit_quantity_total": "HU_QTY_ttl",

    # Item Details with Indexed Fields
    "item_details": {
        "description": "Desc_",
        "hazardous_material": "HM_",
        "weight": "WT_",
        "package_type": "Pkg_Type_",
        "package_quantity": "Pkg_QTY_",
        "handling_unit_type": "HU_Type_",
        "handling_unit_quantity": "HU_QTY_",
        "additional_info": "AddInfo_",
        "pallet": "Pallet_"
    },

    # Totals and Additional Information
    "total_weight": "Total_Weight",
    "total_packages": "TotalPkgs",

    # Transport and Carrier Information
    "master_bol": "MasterBOL",
    "third_party": "3rdParty",
    "collect": "Collect",
    "prepaid": "PrePaid",
    "pro_number": "PRO",
    "scac": "SCAC",
    "seal_number": "SealNum",
    "trailer_number": "TrailerNum",
    "carrier_name": "CarrierName",
    "bol_number": "BOLnum",

    # Billing Information
    "billing_instructions": "BillInstructions",
    "billing_city_state_zip": "BillCityStateZip",
    "billing_address": "BillAddress",
    "billing_name": "BillName",

    # Destination Information
    "to_fob": "ToFOB",
    "to_customer_id": "ToCID",
    "to_city_state_zip": "ToCityStateZip",
    "to_address": "ToAddress",
    "to_location_number": "ToLocNum",
    "to_name": "ToName",

    # Origin Information
    "from_fob": "FromFOB",
    "from_sid_number": "FromSIDNum",
    "from_city_state_zip": "FromCityStateZip",
    "from_address": "FromAddr",
    "from_name": "FromName",

    # Document Information
    "page_total": "Page_ttl",
    "date": "Date",

    # Freight Classification
    "nmfc_codes": ["NMFC2", "NMFC3", "NMFC4", "NMFC5", "NMFC6", "NMFC7", "NMFC8"],
    "class_codes": ["Class2", "Class3", "Class4", "Class5", "Class6", "Class7", "Class8"],

    # Control
    "cover": "cover",
    "reset": "Reset",
    "print_document": "Print"
}

def generate_mapped_data(json_data):
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
            if isinstance(pdf_field, str):  # Direct mapping
                mapped_data[pdf_field] = json_data[json_key]
            elif isinstance(pdf_field, list) and isinstance(json_data[json_key], list):  # List fields like nmfc_codes
                for idx, value in enumerate(json_data[json_key]):
                    if idx < len(pdf_field):
                        mapped_data[pdf_field[idx]] = value

    # Item details with indexed fields
    if "item_details" in json_data:
        for idx, item in enumerate(json_data["item_details"], start=1):
            for item_key, pdf_field_base in field_mapping["item_details"].items():
                if item_key in item:
                    field_name = f"{pdf_field_base}{idx}"
                    mapped_data[field_name] = item[item_key]

    return mapped_data