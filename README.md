# Blockchain Analytics Tool

A comprehensive tool for analyzing blockchain transactions and wallet activities across multiple networks.

## Features

- Multi-chain support (Ethereum, BSC, Polygon)
- Wallet address tracking and analysis
- DeFi protocol interaction detection
- Transaction pattern analysis
- Interactive data visualizations
- Real-time balance checking
- Transaction history charts

## Tech Stack

- **Backend**: Python, FastAPI, Web3.py, SQLAlchemy
- **Frontend**: React, TypeScript, Chart.js
- **Database**: PostgreSQL/SQLite
- **APIs**: Etherscan, Alchemy
- **Deployment**: Docker, Nginx

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Etherscan API key (optional)
- Alchemy API key (optional)

### Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/RobertxMiller/blockchain-analytics-tool.git
cd blockchain-analytics-tool
```

2. Create environment file:
```bash
cp backend/.env.example .env
# Edit .env with your API keys (optional)
```

3. Start the application:
```bash
docker-compose up -d
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## API Usage

### Analyze Wallet
```
GET /api/wallet/analyze/{address}
```

### List Tracked Wallets
```
GET /api/wallet/list
```

## Configuration

Set the following environment variables:
- `ETHERSCAN_API_KEY`: Your Etherscan API key
- `ALCHEMY_URL`: Your Alchemy RPC URL
- `DATABASE_URL`: Database connection string

## Development Status

✅ Core wallet analysis features  
✅ Transaction visualization  
✅ Docker deployment setup  
🚧 Multi-chain support in progress