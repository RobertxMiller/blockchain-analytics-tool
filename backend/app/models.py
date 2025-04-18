from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    tx_hash = Column(String(66), unique=True, index=True)
    block_number = Column(Integer, index=True)
    from_address = Column(String(42), index=True)
    to_address = Column(String(42), index=True)
    value = Column(Float)
    gas_used = Column(Integer)
    gas_price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    network = Column(String(20), default="ethereum")
    
class WalletAddress(Base):
    __tablename__ = "wallet_addresses"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(42), unique=True, index=True)
    label = Column(String(100))
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime)
    total_transactions = Column(Integer, default=0)
    is_contract = Column(Boolean, default=False)
    network = Column(String(20), default="ethereum")