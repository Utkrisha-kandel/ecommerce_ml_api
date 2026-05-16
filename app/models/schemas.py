from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

app = FastAPI()

class UserCreate(BaseModel):
    name:str = Field(min_length=1)
    email:EmailStr
    password: str=Field(min_length=8)

class UserResponse(BaseModel):
    user_id:str
    name:str
    email:str

class ProductCreate(BaseModel):
    name:str=Field(min_length=1, max_length=100)
    price:float = Field(gt=0)
    quantity:int = Field(gt=0)
    description:Optional[str]=None

class ProductResponse(BaseModel):
    product_id:str
    name:str 
    price:float 
    quantity:int
    description:Optional[str]=None
    image:Optional[str]=None

class CartCreate(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)

class CartResponse(BaseModel):
    cart_id: str
    user_id: str
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    product_id:str
    quantity:int = Field(gt=0)

class OrderResponse(BaseModel):
    order_id: str
    user_id: str
    product_id: str
    quantity: int
    total_price: float
    status: str


class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1)


class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float = Field(..., ge=0, le=1)






