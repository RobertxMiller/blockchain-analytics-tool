import requests
import os
from web3 import Web3
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class BlockchainService:
    def __init__(self):
        self.etherscan_api_key = os.getenv("ETHERSCAN_API_KEY")
        self.alchemy_url = os.getenv("ALCHEMY_URL", "")
        
        # Initialize Web3 connection
        if self.alchemy_url:
            self.w3 = Web3(Web3.HTTPProvider(self.alchemy_url))
        else:
            self.w3 = None
    
    async def get_address_transactions(self, address: str, limit: int = 10) -> List[Dict]:
        """Fetch recent transactions for an address using Etherscan API"""
        if not self.etherscan_api_key:
            return []
        
        url = "https://api.etherscan.io/api"
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "page": 1,
            "offset": limit,
            "sort": "desc",
            "apikey": self.etherscan_api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get("status") == "1":
                return data.get("result", [])
        except Exception as e:
            print(f"Error fetching transactions: {e}")
        
        return []
    
    async def get_address_balance(self, address: str) -> Optional[float]:
        """Get current ETH balance for an address"""
        if not self.w3 or not self.w3.is_connected():
            return None
        
        try:
            balance_wei = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return float(balance_eth)
        except Exception as e:
            print(f"Error getting balance: {e}")
            return None
    
    async def check_if_contract(self, address: str) -> bool:
        """Check if address is a smart contract"""
        if not self.w3 or not self.w3.is_connected():
            return False
        
        try:
            code = self.w3.eth.get_code(address)
            return len(code) > 0
        except Exception:
            return False
    
    def format_transaction(self, tx_data: Dict) -> Dict:
        """Format raw transaction data from API"""
        return {
            "hash": tx_data.get("hash"),
            "block_number": int(tx_data.get("blockNumber", 0)),
            "from_address": tx_data.get("from", "").lower(),
            "to_address": tx_data.get("to", "").lower(),
            "value": float(tx_data.get("value", 0)) / 1e18,  # Convert wei to ETH
            "gas_used": int(tx_data.get("gasUsed", 0)),
            "gas_price": float(tx_data.get("gasPrice", 0)) / 1e9,  # Convert to Gwei
            "timestamp": datetime.fromtimestamp(int(tx_data.get("timeStamp", 0)))
        }