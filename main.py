from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import pickle
import numpy as np
from database import get_db, create_tables, Prediction

# Load the trained model when the API starts
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)

class Transaction(BaseModel):
    amount: float
    hour: int
    day_of_week: int
    distance_from_home: float

@app.get("/")
def read_root():
    return {"message": "Hello! Your ML Serving API is alive!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict(transaction: Transaction, db: Session = Depends(get_db)):
    features = np.array([[
        transaction.amount,
        transaction.hour,
        transaction.day_of_week,
        transaction.distance_from_home
    ]])

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]

    result = "fraud" if prediction == 1 else "legitimate"
    fraud_prob = round(float(probability[1]), 4)
    legit_prob = round(float(probability[0]), 4)

    # Save to database
    db_prediction = Prediction(
        amount=transaction.amount,
        hour=transaction.hour,
        day_of_week=transaction.day_of_week,
        distance_from_home=transaction.distance_from_home,
        prediction=result,
        fraud_probability=fraud_prob,
        legitimate_probability=legit_prob
    )
    db.add(db_prediction)
    db.commit()

    return {
        "prediction": result,
        "fraud_probability": fraud_prob,
        "legitimate_probability": legit_prob
    }

@app.get("/predictions")
def get_predictions(db: Session = Depends(get_db)):
    predictions = db.query(Prediction).all()
    return predictions