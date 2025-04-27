import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import './TransactionChart.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

interface Transaction {
  hash: string;
  block_number: number;
  from_address: string;
  to_address: string;
  value: number;
  timestamp: string;
  gas_used: number;
}

interface TransactionChartProps {
  transactions: Transaction[];
  walletAddress: string;
}

const TransactionChart: React.FC<TransactionChartProps> = ({ 
  transactions, 
  walletAddress 
}) => {
  if (!transactions || transactions.length === 0) {
    return (
      <div className="transaction-chart">
        <h3>Transaction Activity</h3>
        <p className="no-data">No recent transaction data available</p>
      </div>
    );
  }

  // Process transaction data for charts
  const processedData = transactions.map(tx => {
    const date = new Date(tx.timestamp).toLocaleDateString();
    const isIncoming = tx.to_address.toLowerCase() === walletAddress.toLowerCase();
    const value = isIncoming ? tx.value : -tx.value;
    
    return {
      date,
      value,
      type: isIncoming ? 'Received' : 'Sent',
      gasUsed: tx.gas_used,
      hash: tx.hash.substring(0, 10) + '...'
    };
  });

  // Line chart data for transaction values over time
  const lineChartData = {
    labels: processedData.map(d => d.date),
    datasets: [
      {
        label: 'Transaction Value (ETH)',
        data: processedData.map(d => Math.abs(d.value)),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1,
      },
    ],
  };

  // Bar chart data for gas usage
  const barChartData = {
    labels: processedData.map(d => d.hash),
    datasets: [
      {
        label: 'Gas Used',
        data: processedData.map(d => d.gasUsed),
        backgroundColor: processedData.map(d => 
          d.type === 'Received' ? 'rgba(54, 162, 235, 0.8)' : 'rgba(255, 99, 132, 0.8)'
        ),
        borderColor: processedData.map(d => 
          d.type === 'Received' ? 'rgba(54, 162, 235, 1)' : 'rgba(255, 99, 132, 1)'
        ),
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="transaction-chart">
      <h3>Transaction Activity</h3>
      
      <div className="chart-container">
        <div className="chart-section">
          <h4>Transaction Values Over Time</h4>
          <Line data={lineChartData} options={chartOptions} />
        </div>
        
        <div className="chart-section">
          <h4>Gas Usage by Transaction</h4>
          <Bar data={barChartData} options={chartOptions} />
        </div>
      </div>

      <div className="transaction-list">
        <h4>Recent Transactions</h4>
        <div className="transaction-items">
          {processedData.map((tx, index) => (
            <div key={index} className={`transaction-item ${tx.type.toLowerCase()}`}>
              <div className="tx-info">
                <span className="tx-hash">{tx.hash}</span>
                <span className={`tx-type ${tx.type.toLowerCase()}`}>
                  {tx.type}
                </span>
              </div>
              <div className="tx-details">
                <span className="tx-value">
                  {Math.abs(tx.value).toFixed(4)} ETH
                </span>
                <span className="tx-date">{tx.date}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TransactionChart;