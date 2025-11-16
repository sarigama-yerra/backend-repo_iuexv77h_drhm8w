"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Lead(BaseModel):
    """
    Leads captured from popups and contact forms
    Collection name: "lead"
    """
    name: Optional[str] = Field(None, description="Full name of the lead")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="WhatsApp/Phone number in international format")
    source: Optional[str] = Field(None, description="Where the lead came from, e.g., popup, contact, booking")
    message: Optional[str] = Field(None, description="Optional message from the user")

class Project(BaseModel):
    """
    Investment projects to showcase
    Collection name: "project"
    """
    name: str = Field(..., description="Project name")
    location: Optional[str] = Field(None, description="City / Area")
    developer: Optional[str] = Field(None, description="Developer brand e.g., Wyndham, JW Marriott, Kamah")
    ownership_options: Optional[List[str]] = Field(default=None, description="List of ownership options e.g., Studio, 1BHK, Villa")
    investment_starts_from: Optional[str] = Field(None, description="Starting investment, human readable e.g., $50,000")
    benefits: Optional[List[str]] = Field(default=None, description="List of benefits for investors")
    photos: Optional[List[str]] = Field(default=None, description="Array of image URLs")
    map_embed_url: Optional[str] = Field(None, description="Google Maps embed URL for the project location")

# Example schemas (kept for reference and potential future use)
class User(BaseModel):
    name: str
    email: EmailStr
    address: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=120)
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    category: str
    in_stock: bool = True
