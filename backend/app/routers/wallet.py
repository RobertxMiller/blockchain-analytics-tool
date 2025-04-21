from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import requests
from .. import schemas, models
from ..database import get_db
from ..services.blockchain import BlockchainService

router = APIRouter(prefix="/wallet", tags=["wallet"])

@router.get("/analyze/{address}", response_model=dict)
async def analyze_wallet(address: str, db: Session = Depends(get_db)):
    """Analyze wallet address and return comprehensive stats"""
    
    if not address.startswith("0x") or len(address) != 42:
        raise HTTPException(status_code=400, detail="Invalid Ethereum address format")
    
    blockchain_service = BlockchainService()
    
    # Check if wallet exists in database
    wallet = db.query(models.WalletAddress).filter(
        models.WalletAddress.address == address.lower()
    ).first()
    
    if not wallet:
        # Create new wallet record
        is_contract = await blockchain_service.check_if_contract(address)
        wallet_data = schemas.WalletAddressCreate(
            address=address.lower(),
            is_contract=is_contract
        )
        wallet = models.WalletAddress(**wallet_data.dict())
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    
    # Get transaction count from database
    tx_count = db.query(models.Transaction).filter(
        (models.Transaction.from_address == address.lower()) |
        (models.Transaction.to_address == address.lower())
    ).count()
    
    # Get current balance
    current_balance = await blockchain_service.get_address_balance(address)
    
    # Get recent transactions from blockchain API
    recent_txs = await blockchain_service.get_address_transactions(address, limit=5)
    
    return {
        "address": address,
        "transaction_count": tx_count,
        "current_balance": current_balance,
        "first_seen": wallet.first_seen,
        "last_activity": wallet.last_activity,
        "is_contract": wallet.is_contract,
        "network": wallet.network,
        "recent_transactions": recent_txs[:3]  # Just show 3 most recent
    }

@router.get("/list", response_model=List[schemas.WalletAddress])
async def list_wallets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of tracked wallet addresses"""
    wallets = db.query(models.WalletAddress).offset(skip).limit(limit).all()
    return wallets