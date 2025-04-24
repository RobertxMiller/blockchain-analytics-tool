import React, { useState } from 'react';
import axios from 'axios';
import './WalletSearch.css';

interface WalletData {
  address: string;
  transaction_count: number;
  current_balance: number | null;
  first_seen: string;
  is_contract: boolean;
  network: string;
  recent_transactions: any[];
}

const WalletSearch: React.FC = () => {
  const [address, setAddress] = useState('');
  const [walletData, setWalletData] = useState<WalletData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!address.trim()) {
      setError('Please enter a wallet address');
      return;
    }

    if (!address.startsWith('0x') || address.length !== 42) {
      setError('Please enter a valid Ethereum address');
      return;
    }

    setLoading(true);
    setError('');
    setWalletData(null);

    try {
      const response = await axios.get(`http://localhost:8000/api/wallet/analyze/${address}`);
      setWalletData(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze wallet');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="wallet-search">
      <div className="search-container">
        <h2>Wallet Analysis</h2>
        <div className="input-group">
          <input
            type="text"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter Ethereum address (0x...)"
            className="address-input"
          />
          <button 
            onClick={handleSearch} 
            disabled={loading}
            className="search-button"
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
        
        {error && <div className="error-message">{error}</div>}
      </div>

      {walletData && (
        <div className="wallet-results">
          <h3>Wallet Information</h3>
          <div className="wallet-info">
            <div className="info-row">
              <span className="label">Address:</span>
              <span className="value">{walletData.address}</span>
            </div>
            <div className="info-row">
              <span className="label">Type:</span>
              <span className="value">
                {walletData.is_contract ? 'Smart Contract' : 'Wallet Address'}
              </span>
            </div>
            <div className="info-row">
              <span className="label">Network:</span>
              <span className="value">{walletData.network}</span>
            </div>
            <div className="info-row">
              <span className="label">Balance:</span>
              <span className="value">
                {walletData.current_balance !== null 
                  ? `${walletData.current_balance.toFixed(4)} ETH`
                  : 'N/A'
                }
              </span>
            </div>
            <div className="info-row">
              <span className="label">Transactions:</span>
              <span className="value">{walletData.transaction_count}</span>
            </div>
            <div className="info-row">
              <span className="label">First Seen:</span>
              <span className="value">
                {new Date(walletData.first_seen).toLocaleDateString()}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default WalletSearch;