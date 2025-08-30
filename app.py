# app/app.py
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base  # ✅ absolute import
import uvicorn

DATABASE_URL = "sqlite:///./ads.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meta Ad Library Bot")

@app.get("/")
def root():
    return {"message": "Meta Ad Bot is running 🚀"}

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)
