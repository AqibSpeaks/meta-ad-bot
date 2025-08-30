# app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Ad(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Meta Ad Library fields
    ad_id = Column(String, unique=True, index=True)  # Unique ID from Meta
    country = Column(String, index=True)
    category = Column(String, index=True)
    ad_copy = Column(Text)
    creative_url = Column(String)  # Thumbnail/video URL
    landing_page = Column(String)

    # Performance metrics
    spending = Column(Float, nullable=True)
    comments = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)

    # Duration
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    # Extra tracking
    last_seen = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Ad(ad_id={self.ad_id}, country={self.country}, category={self.category})>"
