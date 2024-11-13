from pydantic import BaseModel, Field
from typing import List, Optional

class ItemDetail(BaseModel):
    description: Optional[str] = Field(None, alias="Desc")
    hazardous_material: Optional[str] = Field(None, alias="HM")
    weight: Optional[str] = Field(None, alias="WT")
    package_type: Optional[str] = Field(None, alias="Pkg_Type")
    package_quantity: Optional[str] = Field(None, alias="Pkg_QTY")
    handling_unit_type: Optional[str] = Field(None, alias="HU_Type")
    handling_unit_quantity: Optional[str] = Field(None, alias="HU_QTY")
    additional_info: Optional[str] = Field(None, alias="AddInfo")
    pallet: Optional[bool] = Field(None, alias="Pallet")  # Radio button

class BOLData(BaseModel):
    # General Terms Checkboxes
    customer_accept_terms: Optional[bool] = Field(None, alias="Customer_Accept_Terms")
    term_prepaid: Optional[bool] = Field(None, alias="Term_Pre")
    term_collect: Optional[bool] = Field(None, alias="Term_Collect")

    # Payment and Charges Text Fields
    cash_on_delivery: Optional[str] = Field(None, alias="Cash_On_Delivery")
    percentage: Optional[str] = Field(None, alias="Percentage")
    amount: Optional[str] = Field(None, alias="Amt")
    weight_total: Optional[str] = Field(None, alias="Weight_Total")
    package_quantity_total: Optional[str] = Field(None, alias="Pkg_QTY_ttl")
    handling_unit_quantity_total: Optional[str] = Field(None, alias="HU_QTY_ttl")

    # Item Details (repeating fields handled as a list of ItemDetail instances)
    item_details: List[ItemDetail] = Field(default_factory=list)

    # Totals and Additional Information
    total_weight: Optional[str] = Field(None, alias="Total_Weight")
    total_packages: Optional[str] = Field(None, alias="TotalPkgs")

    # Transport and Carrier Information Text Fields
    master_bol: Optional[bool] = Field(None, alias="MasterBOL")
    third_party: Optional[str] = Field(None, alias="3rdParty")
    collect: Optional[str] = Field(None, alias="Collect")
    prepaid: Optional[str] = Field(None, alias="PrePaid")
    pro_number: Optional[str] = Field(None, alias="PRO")
    scac: Optional[str] = Field(None, alias="SCAC")
    seal_number: Optional[str] = Field(None, alias="SealNum")
    trailer_number: Optional[str] = Field(None, alias="TrailerNum")
    carrier_name: Optional[str] = Field(None, alias="CarrierName")
    bol_number: Optional[str] = Field(None, alias="BOLnum")

    # Billing Information
    billing_instructions: Optional[str] = Field(None, alias="BillInstructions", description="Leave this empty this isn't there")
    billing_city_state_zip: Optional[str] = Field(None, alias="BillCityStateZip", description="Leave this empty this isn't there")
    billing_address: Optional[str] = Field(None, alias="BillAddress", description="Leave this empty this isn't there")
    billing_name: Optional[str] = Field(None, alias="BillName", description="Leave this empty this isn't there")

    # Destination Information
    to_fob: Optional[bool] = Field(None, alias="ToFOB", description="This is the shipping address")
    to_customer_id: Optional[str] = Field(None, alias="ToCID", description="This is the shipping customer id ")
    to_city_state_zip: Optional[str] = Field(None, alias="ToCityStateZip", description="This is the shipping destination zip")
    to_address: Optional[str] = Field(None, alias="ToAddress",description="This is the shipping to address")
    to_location_number: Optional[str] = Field(None, alias="ToLocNum", description="This is the shipping to location number")
    to_name: Optional[str] = Field(None, alias="ToName", description="this is the shipping to name")

    # Origin Information
    from_fob: Optional[bool] = Field(None, alias="FromFOB")
    from_sid_number: Optional[str] = Field(None, alias="FromSIDNum")
    from_city_state_zip: Optional[str] = Field(None, alias="FromCityStateZip")
    from_address: Optional[str] = Field(None, alias="FromAddr")
    from_name: Optional[str] = Field(None, alias="FromName")

    # Document Information
    page_total: Optional[str] = Field(None, alias="Page_ttl")
    date: Optional[str] = Field(None, alias="Date")

    # Freight Classification (NMFC and Class codes for up to 8 items)
    nmfc_codes: List[Optional[str]] = Field(default_factory=lambda: [None] * 8)
    class_codes: List[Optional[str]] = Field(default_factory=lambda: [None] * 8)

    # Control Checkboxes
    cover: Optional[bool] = Field(None, alias="cover")
    reset: Optional[bool] = Field(None, alias="Reset")
    print_document: Optional[bool] = Field(None, alias="Print")


