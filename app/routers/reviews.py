from fastapi import APIRouter, HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import Depends

from app.ml.train_sentiment import predict_sentiment
from app.models.models import Product, Review
from app.models.schemas import ReviewResponse,ReviewCreate
from app.utils.oauth2 import get_current_user
import uuid
from typing import List


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)
@router.post("/{product_id}",status_code=status.HTTP_201_CREATED,response_model=ReviewResponse)
def create_review(product_id:str,review:ReviewCreate,db:Session=Depends(get_db),current_user = Depends(get_current_user)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")
    sentiment_result = predict_sentiment(review.text)
    new_review = Review(
        review_id=str(uuid.uuid4()),
        user_id=current_user.user_id,
        product_id=product_id,
        text=review.text,
        sentiment=sentiment_result["sentiment"],
        confidence=sentiment_result["confidence"],
        rating=review.rating
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

#Get all reviews for a product
@router.get("/product/{product_id}", response_model=List[ReviewResponse]) 
def get_product_reviews(product_id:str, db:Session=Depends(get_db)):
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    if not reviews:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No reviews found for this product")
    return reviews
#GEt sentiments for a product
@router.get("/product/{product_id}/summary")
def get_sentiment_summary(product_id:str, db:Session=Depends(get_db)):
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    if not reviews:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No reviews found for this product")
    total_reviews = len(reviews)
    positive = len([r for r in reviews if r.sentiment == "positive"])
    negative = total_reviews - positive
    avg_confidence = sum(r.confidence for r in reviews) / total_reviews
    avg_rating = sum(r.rating for r in reviews) / total_reviews
    return {
        "product_id": product_id,
        "total_reviews": total_reviews,
        "positive_reviews": positive,
        "negative_reviews": negative,
        "average_confidence": round(avg_confidence, 4),
        "average_rating": round(avg_rating, 2)
    }
#Delete Review
@router.delete("/{review_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id:str, db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    review = db.query(Review).filter(Review.review_id == review_id, Review.user_id == current_user.user_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Review not found or not authorized to delete")
    if review.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to delete this review")
    db.delete(review)
    db.commit()
    return