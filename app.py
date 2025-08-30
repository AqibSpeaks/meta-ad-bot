# app/app.py
from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = "sqlite:///ads.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Meta Ad Library Bot API is running 🚀"}
