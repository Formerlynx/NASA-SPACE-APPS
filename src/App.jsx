import { useState, useEffect } from 'react';
import { WASTE_TYPES, CONVERSION_METHODS } from './data';
import { calculateConversion } from './utils';
import InputPanel from './components/InputPanel';
import ResultsPanel from './components/ResultsPanel';
import './App.css';

function App() {
  const [wasteType, setWasteType] = useState(WASTE_TYPES[0]);
  const [mass, setMass] = useState('200');
  const [conversionMethod, setConversionMethod] = useState(CONVERSION_METHODS[0]);
  const [results, setResults] = useState(null);

  useEffect(() => {
    runSimulation();
  }, []);

  const runSimulation = () => {
    const massValue = parseFloat(mass);

    if (isNaN(massValue) || massValue <= 0) {
      alert('Please enter a valid mass greater than 0');
      return;
    }

    const simulationResults = calculateConversion(wasteType, massValue, conversionMethod);
    setResults(simulationResults);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>PROMETHEUS</h1>
        <p>Waste-to-Fuel Simulator</p>
      </header>

      <main className="app-main">
        <InputPanel
          wasteType={wasteType}
          setWasteType={setWasteType}
          mass={mass}
          setMass={setMass}
          conversionMethod={conversionMethod}
          setConversionMethod={setConversionMethod}
          onRunSimulation={runSimulation}
        />

        <ResultsPanel results={results} />
      </main>
    </div>
  );
}

export default App;
