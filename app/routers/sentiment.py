from fastapi import APIRouter
from app.models.schemas import SentimentRequest, SentimentResponse
from app.ml.train_sentiment import predict_sentiment, train_sentiment_model

router = APIRouter(
    prefix="/sentiment",
    tags=["Sentiment"]
)


@router.post("/predict", response_model=SentimentResponse)
def predict(request: SentimentRequest):
    """Predict the sentiment of a text input."""
    return predict_sentiment(request.text)


@router.post("/train")
def train():
    """Train or retrain the sentiment analysis model."""
    train_sentiment_model()
    return {"message": "Sentiment model trained successfully."}
