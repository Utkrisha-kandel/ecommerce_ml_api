from fastapi import FastAPI
from app.database import engine
from app.models import models
from app.routers import users
from app.routers import products, orders, cart, auth, sentiment
from fastapi.staticfiles import StaticFiles
# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ecommerce ML API",
    description="Ecommerce API with ML features",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(cart.router)
app.include_router(sentiment.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")




@app.get("/")
def root():
    return {"message": "Welcome to Ecommerce ML API"}