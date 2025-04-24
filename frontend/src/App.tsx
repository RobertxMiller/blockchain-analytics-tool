import React from 'react';
import './App.css';
import WalletSearch from './components/WalletSearch';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Blockchain Analytics Tool</h1>
        <p>Analyze blockchain transactions and wallet activities</p>
      </header>
      <main>
        <WalletSearch />
      </main>
    </div>
  );
}

export default App;