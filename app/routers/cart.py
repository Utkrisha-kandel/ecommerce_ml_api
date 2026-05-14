from fastapi import APIRouter, status, HTTPException, Depends
from app.models.schemas import CartCreate, CartResponse
from app.database import get_db
from typing import List
import uuid
from sqlalchemy.orm import Session
from app.models.models import Cart, Product

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


# ADD TO CART
from app.utils.oauth2 import get_current_user
from app.models.models import User

# ADD TO CART
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CartResponse)
def add_to_cart(cart: CartCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.product_id == cart.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    if product.quantity < cart.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock"
        )
    existing = db.query(Cart).filter(
        Cart.user_id == current_user.user_id,
        Cart.product_id == cart.product_id
    ).first()
    if existing:
        existing.quantity += cart.quantity
        db.commit()
        db.refresh(existing)
        return existing

    new_cart = Cart(
        cart_id=str(uuid.uuid4()),
        user_id=current_user.user_id,  # from JWT token
        product_id=cart.product_id,
        quantity=cart.quantity
    )
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart


# GET CART
@router.get("/", response_model=List[CartResponse])
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Cart).filter(Cart.user_id == current_user.user_id).all()


# GET CART
@router.get("/", response_model=List[CartResponse])
def get_cart(user_id: str, db: Session = Depends(get_db)):
    return db.query(Cart).filter(Cart.user_id == user_id).all()


# REMOVE FROM CART
@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(cart_id: str, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    db.delete(cart)
    db.commit()
    return


# CLEAR CART
@router.delete("/clear/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(user_id: str, db: Session = Depends(get_db)):
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()
    return