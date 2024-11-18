from pydantic import BaseModel, Field
from typing import List, Optional

class ItemDetail(BaseModel):
    origin: Optional[str] = Field(None, alias="Origin")
    commodity_description: Optional[str] = Field(None, alias="Commodity_Description")
    schedule_b_or_hts: Optional[str] = Field(None, alias="Schedule_B_or_HTS")
    eccn_or_usml_category: Optional[str] = Field(None, alias="ECCN_or_USML_Category")
    quantity_top: Optional[str] = Field(None, alias="Quantity_Top")
    uom_top: Optional[str] = Field(None, alias="UOM_Top")
    gross_weight: Optional[str] = Field(None, alias="Gross_Weight")
    gross_weight_dropdown: Optional[str] = Field(None, alias="Gross_Weight_Dropdown")
    export_value: Optional[str] = Field(None, alias="Export_Value")
    license_or_cfr: Optional[str] = Field(None, alias="Lic_or_CFR")
    sme: Optional[bool] = Field(None, alias="SME")
    ddtc_qty_uom: Optional[str] = Field(None, alias="DDTC_Qty_UOM")
    quantity_bottom: Optional[str] = Field(None, alias="Quantity_Bottom")
    uom_bottom: Optional[str] = Field(None, alias="UOM_Bottom")
    license_value: Optional[str] = Field(None, alias="License_Value")

class ExpeditorsSLIData(BaseModel):
    # General Information
    reference_number: Optional[str] = Field(None, alias="Reference_#")
    contact_name: Optional[str] = Field(None, alias="Contact_Name")
    contact_phone: Optional[str] = Field(None, alias="Contact_Phone")

    # Principal Party Information
    principle_party_name: Optional[str] = Field(None, alias="PRINCIPLE_PARTY_IN_INTEREST_Name")
    principle_party_ein: Optional[str] = Field(None, alias="PRINCIPLE_PARTY_IN_INTEREST_EIN")
    principle_party_address: Optional[str] = Field(None, alias="PRINCIPLE_PARTY_IN_INTEREST_Address_Cargo_Location")
    principle_party_state_of_origin: Optional[str] = Field(None, alias="PRINCIPLE_PARTY_IN_INTEREST_State_of_Origin")

    # Ultimate Consignee Information
    ultimate_consignee_type: Optional[str] = Field(None, alias="ULTIMATE_CONSIGNEE_Consignee_Type")
    ultimate_consignee_name_address: Optional[str] = Field(None, alias="ULTIMATE_CONSIGNEE_Name/Address")
    ultimate_consignee_country_destination: Optional[str] = Field(None, alias="ULTIMATE_CONSIGNEE_Country_of_Ultimate_Destination")
    ultimate_consignee_fppi_name: Optional[str] = Field(None, alias="ULTIMATE_CONSIGNEE_FPPI_Name")

    # Conditional Fields
    related_parties: Optional[bool] = Field(None, alias="Related_Parties")
    routed_export_transaction: Optional[bool] = Field(None, alias="Routed_Export_Transaction")
    hazardous_materials: Optional[bool] = Field(None, alias="Hazardous_Materials")
    ftz_identifier: Optional[str] = Field(None, alias="OTHER_CONDITIONAL_FTZ_Identifier")
    intermediate_consignee: Optional[str] = Field(None, alias="OTHER_CONDITIONAL_Intermediate_Consignee_Name_&_Address")
    entry_number: Optional[str] = Field(None, alias="OTHER_CONDITIONAL_Entry_#")

    # Transportation Information
    method_of_transportation: Optional[str] = Field(None, alias="Method_of_Transportation")
    port_of_export: Optional[str] = Field(None, alias="Port_of_Export")
    port_of_unlading: Optional[str] = Field(None, alias="Port_of_Unlading")
    vessel_name: Optional[str] = Field(None, alias="Vessel_Name")
    date_of_export: Optional[str] = Field(None, alias="Date_of_Export")

    # Charges
    charges_freight: Optional[str] = Field(None, alias="Charges_Freight")
    charges_duty: Optional[str] = Field(None, alias="Charges_Duty")
    charges_tax: Optional[str] = Field(None, alias="Charges_Tax")
    charges_customs: Optional[str] = Field(None, alias="Charges_Customs")

    # Insurance
    insurance_requested: Optional[bool] = Field(None, alias="Insurance_Requested")
    amount_of_insurance: Optional[str] = Field(None, alias="Amount_of_Insurance")
    declared_value_for_carriage: Optional[str] = Field(None, alias="Declared_Value_for_Carriage")

    # Items Details
    items: List[ItemDetail] = Field(default_factory=list)

    # Signature
    title: Optional[str] = Field(None, alias="Title")
    signature_date: Optional[str] = Field(None, alias="Signature_Date")

