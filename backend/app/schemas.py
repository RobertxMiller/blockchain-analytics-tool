from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    tx_hash: str
    block_number: int
    from_address: str
    to_address: str
    value: float
    gas_used: int
    gas_price: float
    network: str = "ethereum"

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class WalletAddressBase(BaseModel):
    address: str
    label: Optional[str] = None
    network: str = "ethereum"

class WalletAddressCreate(WalletAddressBase):
    pass

class WalletAddress(WalletAddressBase):
    id: int
    first_seen: datetime
    last_activity: Optional[datetime] = None
    total_transactions: int = 0
    is_contract: bool = False
    
    class Config:
        from_attributes = True