import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

BASE_PATH = Path(__file__).resolve().parent
PIPELINE_PATH = BASE_PATH / "sentiment_pipeline.joblib"


DEFAULT_TRAINING_DATA = [
    # Positive reviews
    {"text": "I love this product, it works perfectly and makes me happy.", "label": 1},
    {"text": "Absolutely fantastic quality and amazing service.", "label": 1},
    {"text": "This is the best purchase I have made in a long time.", "label": 1},
    {"text": "I am very satisfied with the results.", "label": 1},
    {"text": "It exceeded my expectations and I would buy it again.", "label": 1},
    {"text": "good product i love it", "label": 1},
    {"text": "works great highly recommend", "label": 1},
    {"text": "amazing quality very happy with purchase", "label": 1},
    {"text": "excellent product fast delivery", "label": 1},
    {"text": "best product ever bought", "label": 1},
    {"text": "very good quality worth the money", "label": 1},
    {"text": "happy with this purchase will buy again", "label": 1},
    {"text": "great product works as described", "label": 1},
    {"text": "super fast delivery and good quality", "label": 1},
    {"text": "highly recommend this to everyone", "label": 1},
    {"text": "perfect product exactly what i needed", "label": 1},
    {"text": "outstanding quality very impressed", "label": 1},
    {"text": "love it so much works perfectly fine", "label": 1},
    {"text": "great value for money satisfied", "label": 1},
    {"text": "product is exactly as shown in pictures", "label": 1},
    {"text": "very comfortable and good material", "label": 1},
    {"text": "exceeded all my expectations brilliant", "label": 1},
    {"text": "works like a charm very pleased", "label": 1},
    {"text": "good product good price good quality", "label": 1},
    {"text": "superb quality and excellent packaging", "label": 1},
    {"text": "five stars would definitely buy again", "label": 1},
    {"text": "product arrived quickly and works great", "label": 1},
    {"text": "fantastic purchase very happy customer", "label": 1},
    {"text": "really good product no complaints", "label": 1},
    {"text": "brilliant product does exactly what it says", "label": 1},
    {"text": "very well made and durable product", "label": 1},
    {"text": "amazing product changed my life", "label": 1},
    {"text": "top quality product highly satisfied", "label": 1},
    {"text": "wonderful product great experience overall", "label": 1},
    {"text": "so glad i bought this product love it", "label": 1},

    # Negative reviews
    {"text": "I hate this, it broke on the first day.", "label": 0},
    {"text": "Terrible experience, I am very disappointed.", "label": 0},
    {"text": "The product is awful and does not work at all.", "label": 0},
    {"text": "I regret buying this, it is the worst.", "label": 0},
    {"text": "Such a bad purchase, totally not worth the money.", "label": 0},
    {"text": "bad quality not worth it", "label": 0},
    {"text": "broke after one use terrible", "label": 0},
    {"text": "worst product ever do not buy", "label": 0},
    {"text": "very disappointed with the quality", "label": 0},
    {"text": "complete waste of money terrible product", "label": 0},
    {"text": "stopped working after two days awful", "label": 0},
    {"text": "poor quality not as described", "label": 0},
    {"text": "do not buy this product very bad", "label": 0},
    {"text": "horrible product returned immediately", "label": 0},
    {"text": "defective product very poor quality", "label": 0},
    {"text": "total waste of money not recommended", "label": 0},
    {"text": "product broke immediately very angry", "label": 0},
    {"text": "very bad experience never buying again", "label": 0},
    {"text": "cheap material falls apart easily", "label": 0},
    {"text": "not worth the price very disappointed", "label": 0},
    {"text": "arrived damaged very poor packaging", "label": 0},
    {"text": "does not work as advertised terrible", "label": 0},
    {"text": "worst purchase of my life avoid", "label": 0},
    {"text": "completely useless product waste of money", "label": 0},
    {"text": "very poor quality broke after one week", "label": 0},
    {"text": "disgusting quality never buying again", "label": 0},
    {"text": "false advertising product nothing like pictures", "label": 0},
    {"text": "extremely disappointed with this product", "label": 0},
    {"text": "product is garbage total waste", "label": 0},
    {"text": "broken on arrival very bad experience", "label": 0},
    {"text": "terrible quality do not recommend", "label": 0},
    {"text": "awful product stopped working immediately", "label": 0},
    {"text": "very unhappy with this purchase regret it", "label": 0},
    {"text": "poor build quality very fragile", "label": 0},
    {"text": "not as described complete disappointment", "label": 0},

]

def _load_training_data(csv_path: str = None):
    if csv_path:
        df = pd.read_csv(csv_path)
        if "text" not in df.columns or "label" not in df.columns:
            raise ValueError("Training CSV must contain 'text' and 'label' columns.")
        df = df.dropna(subset=["text", "label"])
        texts = df["text"].astype(str).tolist()
        labels = df["label"].apply(lambda v: 1 if str(v).strip().lower() in ["1", "true", "yes", "positive", "pos"] else 0).tolist()
        return texts, labels

    texts = [item["text"] for item in DEFAULT_TRAINING_DATA]
    labels = [item["label"] for item in DEFAULT_TRAINING_DATA]
    return texts, labels


def train_sentiment_model(csv_path: str = None, save: bool = True):
    texts, labels = _load_training_data(csv_path)
    pipeline = Pipeline([
        ("vectorizer", TfidfVectorizer(ngram_range=(1, 2), stop_words="english")),
        ("classifier", LogisticRegression(solver="liblinear", random_state=42, max_iter=1000)),
    ])
    pipeline.fit(texts, labels)
    if save:
        joblib.dump(pipeline, PIPELINE_PATH)
    return pipeline


def load_sentiment_pipeline():
    if not PIPELINE_PATH.exists():
        return train_sentiment_model()
    return joblib.load(PIPELINE_PATH)


def predict_sentiment(text: str):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must be a non-empty string.")
    pipeline = load_sentiment_pipeline()
    proba = pipeline.predict_proba([text.strip()])[0]
    positive_score = float(proba[1])
    sentiment = "positive" if positive_score >= 0.5 else "negative"
    confidence = positive_score if sentiment == "positive" else float(proba[0])
    return {
        "text": text,
        "sentiment": sentiment,
        "confidence": round(confidence, 4),
    }


if __name__ == "__main__":
    pipeline = train_sentiment_model()
    print(f"Trained sentiment model and saved to: {PIPELINE_PATH}")

