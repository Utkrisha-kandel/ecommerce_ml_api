# Ecommerce ML API

A REST API built with FastAPI for an ecommerce platform. Started this project to learn FastAPI and integrate ML models into a real backend.

## What it does
- User registration and login
- JWT authentication with role based access (admin/user)
- Admin can create, update and delete products
- Users can add products to cart and place orders
- Product reviews with automatic sentiment analysis
- Order confirmation email after placing order
- Product images upload

## Tech used
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- Passlib (bcrypt)
- FastAPI Mail
- Scikit-learn (sentiment analysis)
- Docker

## Project Structure
```
ecommerce-ml-api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   ├── cart.py
│   │   ├── reviews.py
│   │   └── sentiment.py
│   ├── models/
│   │   ├── models.py
│   │   └── schemas.py
│   ├── utils/
│   │   ├── hashing.py
│   │   ├── oauth2.py
│   │   └── email.py
│   └── ml/
│       └── train_sentiment.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env
```

## How to run

### Without Docker

1. Clone the repo
```bash
git clone https://github.com/yourusername/ecommerce-ml-api.git
cd ecommerce-ml-api
```

2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` file
5. Run
```bash
uvicorn app.main:app --reload
```

### With Docker

```bash
docker-compose up --build
```

6. Test at `http://127.0.0.1:8000/docs`

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | Login and get JWT token |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Register new user |
| GET | `/users/` | Get all users |
| GET | `/users/{user_id}` | Get user by ID |
| PUT | `/users/{user_id}` | Update user |
| DELETE | `/users/{user_id}` | Delete user |

### Products
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/products/` | Create product | Admin only |
| GET | `/products/` | Get all products | Public |
| GET | `/products/{product_id}` | Get product by ID | Public |
| PUT | `/products/{product_id}` | Update product | Admin only |
| DELETE | `/products/{product_id}` | Delete product | Admin only |
| POST | `/products/{product_id}/upload-image` | Upload image | Admin only |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/orders/` | Place an order |
| GET | `/orders/` | Get all orders |
| GET | `/orders/{order_id}` | Get order by ID |
| DELETE | `/orders/{order_id}` | Cancel order |

### Cart
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/cart/` | Add to cart |
| GET | `/cart/` | Get cart |
| DELETE | `/cart/{cart_id}` | Remove item |
| DELETE | `/cart/clear/{user_id}` | Clear cart |

### Reviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/reviews/{product_id}` | Add review with auto sentiment |
| GET | `/reviews/product/{product_id}` | Get product reviews |
| GET | `/reviews/product/{product_id}/summary` | Get sentiment summary |
| DELETE | `/reviews/{review_id}` | Delete review |

### Sentiment
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sentiment/predict` | Analyze text sentiment |

## Status
Still adding features — product recommendations and deployment coming soon.