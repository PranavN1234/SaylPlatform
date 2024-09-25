from pydantic import BaseModel, Field
from typing import List, Optional

class Ruling(BaseModel):
    ID: int = Field(description="The unique identifier of the cross ruling document.")
    Title: str = Field(description="The title of the ruling document, describing the product and ruling context.")
    Summary: str = Field(description="A short summary of the ruling, highlighting the key decision or product classification.")
    Tariffs: List[str] = Field(description="A list of tariff codes associated with the product in the ruling.")
    SearchUrl: str = Field(description="The direct search url found in the context to link to the cbp for that ruling number")
    URL: str = Field(description="The URL to access the full ruling document.")  # Changed to str

class CrossRulingsResponse(BaseModel):
    message: str = Field(description="A friendly message or brief introduction summarizing the cross rulings provided.")
    intent: str = Field(description="The detected intent, which is 'cross_rulings_inquiry' for this response.")  # Removed default
    product: str = Field(description="The product name extracted from the user query, possibly including details such as country or packaging.")
    best_ruling: Optional[Ruling] = Field(description="10 digit HTS Code, make sure you include both the heading and suffix to the best ruling")
    related_rulings: List[Ruling] = Field(description="A list of additional rulings that may be related to the product query.")
    gpt_insights: str = Field(description="Optional GPT-generated insights explaining differences between rulings or other important factors to consider.")

class HTSFootnote(BaseModel):
    marker: str = Field(description="The footnote marker or identifier (e.g., 1)")
    value: str = Field(description="The footnote explanation (e.g., 'See 9903.88.03')")

class HTSCode(BaseModel):
    htsno: str = Field(description="Harmonized Tariff Schedule number for the product")
    description: str = Field(description="Description of the product covered by the HTS code")
    general: Optional[str] = Field(description="General tariff rate")
    special: Optional[str] = Field(description="Special tariff rate if applicable")
    other: Optional[str] = Field(description="Other tariff rates (e.g., for specific countries)")
    units: Optional[List[str]] = Field(description="Units applicable (e.g., kg, liters)")
    footnotes: Optional[List[HTSFootnote]] = Field(description="Footnotes related to special conditions")

class HTSResponse(BaseModel):
    message: str = Field(description="User-friendly message explaining the HTS findings")
    intent: str = Field(description="The intent detected from the user's query")  # Removed default
    product: str = Field(description="The product extracted from the user's query")
    best_hts_code: Optional[HTSCode] = Field(description="The best matching HTS code based on the product description")
    related_hts_codes: List[HTSCode] = Field(description="List of related HTS codes that may also be relevant")
    tariff_insights: str = Field(description="GPT insights on what tarrifs regarding this product")

class GeneralResponse(BaseModel):
    message: str = Field(description="A user-friendly message answering the users queries")

