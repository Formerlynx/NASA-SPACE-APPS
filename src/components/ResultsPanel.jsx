import { formatEnergy, formatMass, formatPercentage } from '../utils';
import EnergyChart from './EnergyChart';
import FuelChart from './FuelChart';
import './ResultsPanel.css';

function ResultsPanel({ results }) {
  if (!results) {
    return (
      <div className="results-panel">
        <div className="no-results">
          <p>Run a simulation to see results</p>
        </div>
      </div>
    );
  }

  return (
    <div className="results-panel">
      <div className="results-header">
        <h2>Simulation Results</h2>
      </div>

      <div className="results-grid">
        <div className="results-card summary-card">
          <h3>Summary</h3>
          <div className="summary-content">
            <div className="summary-item">
              <span className="label">Waste Type:</span>
              <span className="value">{results.wasteType}</span>
            </div>
            <div className="summary-item">
              <span className="label">Mass:</span>
              <span className="value">{formatMass(results.mass)}</span>
            </div>
            <div className="summary-item">
              <span className="label">Method:</span>
              <span className="value">{results.conversionMethod}</span>
            </div>
          </div>
        </div>

        <div className="results-card energy-card">
          <h3>Energy Balance</h3>
          <div className="energy-stats">
            <div className="stat-item">
              <span className="stat-label">Energy Required</span>
              <span className="stat-value input">{formatEnergy(results.energyRequired)}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Energy Output</span>
              <span className="stat-value output">{formatEnergy(results.totalEnergyOutput)}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Net Balance</span>
              <span className={`stat-value ${results.netEnergyBalance >= 0 ? 'positive' : 'negative'}`}>
                {results.netEnergyBalance >= 0 ? '+' : ''}{formatEnergy(results.netEnergyBalance)}
              </span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Efficiency</span>
              <span className="stat-value efficiency">{formatPercentage(results.conversionEfficiency)}</span>
            </div>
          </div>
        </div>

        <div className="results-card fuel-card">
          <h3>Fuel Production</h3>
          <div className="fuel-list">
            {Object.entries(results.fuelProduced).map(([fuelType, amount]) => (
              <div key={fuelType} className="fuel-item">
                <span className="fuel-type">{fuelType.charAt(0).toUpperCase() + fuelType.slice(1)}</span>
                <div className="fuel-details">
                  <span className="fuel-amount">{formatMass(amount)}</span>
                  <span className="fuel-energy">{formatEnergy(results.fuelEnergyOutput[fuelType])}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="results-card chart-card">
          <h3>Energy Balance Chart</h3>
          <EnergyChart results={results} />
        </div>

        <div className="results-card chart-card">
          <h3>Fuel Distribution</h3>
          <FuelChart results={results} />
        </div>
      </div>
    </div>
  );
}

export default ResultsPanel;
