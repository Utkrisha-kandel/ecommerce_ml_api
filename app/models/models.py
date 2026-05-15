from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


# ─── USER TABLE ─────────────────────────────────
class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")

    orders = relationship("Order", back_populates="user")
    cart = relationship("Cart", back_populates="user")



# ─── PRODUCT TABLE ──────────────────────────────
class Product(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)

    orders = relationship("Order", back_populates="product")
    cart = relationship("Cart", back_populates="product")



# ─── ORDER TABLE ────────────────────────────────
class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    product_id = Column(String, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="pending")

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")

class Cart(Base):
    __tablename__ = "cart"

    cart_id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    product_id = Column(String, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    user = relationship("User", back_populates="cart")
    product = relationship("Product", back_populates="cart")