from fastapi import APIRouter, HTTPException, status, Depends,UploadFile ,File
from app.models.schemas import ProductCreate, ProductResponse
from app.database import get_db
from typing import List
import uuid
from sqlalchemy.orm import Session
from app.models.models import Product, User
from app.utils.oauth2 import get_current_admin
import shutil
import os

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# CREATE PRODUCT - admin only
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_admin)):
    existing_product = db.query(Product).filter(Product.name == product.name).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists"
        )
    new_product = Product(
        product_id=str(uuid.uuid4()),
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        description=product.description
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# GET ALL PRODUCTS - anyone
@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


# GET PRODUCT BY ID - anyone
@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # fixed
            detail="Product not found"
        )
    return product


# UPDATE PRODUCT - admin only
@router.put("/{product_id}", response_model=ProductResponse)
def update_product_by_id(product_id: str, name: str = None, price: float = None,
                          quantity: int = None, description: str = None,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_admin)):  # added
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
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


# DELETE PRODUCT - admin only
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_admin)):  # added
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    db.delete(product)
    db.commit()  # fixed - added ()
    return

#UPLOAD PRODUCT IMAGE - ADMIN ONLY
@router.post("/{product_id}/upload-image")
def upload_image(product_id:str, file:UploadFile=File(...),
                 db:Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    if file.content_type not in ["image/jpeg", "image/png", "image/jpeg"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Only Jpeg and png images are allowed"
        )
    folder = "app/static/images"
    os.makedirs(folder, exist_ok=True)
    file_path = f"{folder}/{product_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
        product.image = file_path
    db.commit()
    db.refresh(product)
    return {"message": "Image uploaded", "image_path": file_path}
