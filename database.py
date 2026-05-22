import os
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Connection string — tells SQLAlchemy how to connect to our database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mlapiuser:mlapipassword@localhost/mlapi")

# Create the engine — this is the actual connection to PostgreSQL
engine = create_engine(DATABASE_URL)

# Each database session is like one "conversation" with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all our database models will inherit from
Base = declarative_base()

# This defines the "predictions" table in the database
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    hour = Column(Integer)
    day_of_week = Column(Integer)
    distance_from_home = Column(Float)
    prediction = Column(String)
    fraud_probability = Column(Float)
    legitimate_probability = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# This creates the table in the database if it doesn't exist yet
def create_tables():
    Base.metadata.create_all(bind=engine)

# This gives us a database session to use in our endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()