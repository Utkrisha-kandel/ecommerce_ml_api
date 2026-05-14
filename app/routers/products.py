from fastapi import APIRouter,HTTPException,status,Depends
from app.models.schemas import ProductCreate,ProductResponse
from app.database import get_db
from typing import List
import uuid
from sqlalchemy.orm import Session
from app.models.models import Product

router = APIRouter(
    prefix="/products",
    tags = ["Products"]
)

#CREATing Products

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=ProductResponse)
def create_product(product:ProductCreate, db:Session=Depends(get_db)):
    existing_product = db.query(Product).filter(Product.name == product.name).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Prodcut with this name already exists"
        )
    new_product = Product(
        product_id = str(uuid.uuid4()),
        name = product.name,
        price = product.price,
        quantity = product.quantity,
        description = product.description
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
#GET PRODUCTS 
@router.get("/", response_model=List[ProductResponse])
def get_products(db:Session = Depends(get_db)):
    return db.query(Product).all()

#GET PRODUCTS BY ID
@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id:str,db:Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail= "Product not found")
    return product

#update products by id

@router.put("/{product_id}", response_model=ProductResponse)
def update_product_by_id(product_id:str, name:str = None,price:float = None,quantity:int = None,description:str=None,db:Session=Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if  not product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="User not found")

    if name:
            product.name = name
    if price:
            product.price = price
    if quantity:
            product.quantity = quantity
    if description:
            product.description = description
    db.commit()
    db.refresh(product)
    return product

#delete product
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id:str, db:Session=Depends(get_db)):
     product = db.query(Product).filter(Product.product_id == product_id).first()
     if not product:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
     db.delete(product)
     db.commit
     return