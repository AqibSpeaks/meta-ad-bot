from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base   # ✅ back to relative import since app is now a package

DATABASE_URL = "sqlite:///./ads.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meta Ad Library Bot")

@app.get("/")
def root():
    return {"message": "Meta Ad Bot is running 🚀"}
