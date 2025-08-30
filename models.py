from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    created_at = Column(DateTime)

class AdCampaign(Base):
    __tablename__ = 'ad_campaigns'
    
    id = Column(Integer, primary_key=True)
    campaign_name = Column(String(200))
    budget = Column(Integer)
    status = Column(String(50))
