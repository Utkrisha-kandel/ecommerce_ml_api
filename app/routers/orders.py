from fastapi import APIRouter,status,HTTPException,Depends
from app.models.schemas import OrderCreate, OrderResponse
from app.database import get_db
from typing import List
import uuid
from sqlalchemy.orm import Session
from app.models.models import Order,Product
from app.utils.oauth2 import get_current_user
from app.models.models import User
router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)
#create order
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=OrderResponse)
def create_order(order:OrderCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    product = db.query(Product).filter(Product.product_id == order.product_id).first()
    user_id = current_user.user_id
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Prdouct not found")
    if product.quantity < order.quantity:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "NOT enough stock"
        )
    #calculate total price
    total_price = product.price * order.quantity
    product.quantity -= order.quantity
    new_order = Order(
        order_id = str(uuid.uuid4()),
        user_id = user_id,
        product_id = order.product_id,
        quantity= order.quantity,
        total_price = total_price,
        status="pending"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
    
    #get all orders
@router.get("/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()
#get order by id
@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(order_id:str,db:Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Order not found"
        )
    return order
#cancel order
@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    db.delete(order)
    db.commit()
    return

