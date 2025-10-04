import { WASTE_TYPES, CONVERSION_METHODS } from '../data';
import './InputPanel.css';

function InputPanel({ wasteType, setWasteType, mass, setMass, conversionMethod, setConversionMethod, onRunSimulation }) {
  return (
    <div className="input-panel">
      <h2>Simulation Parameters</h2>

      <div className="input-group">
        <label htmlFor="waste-type">Waste Type</label>
        <select
          id="waste-type"
          value={wasteType}
          onChange={(e) => setWasteType(e.target.value)}
        >
          {WASTE_TYPES.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </div>

      <div className="input-group">
        <label htmlFor="mass">Mass (kg)</label>
        <input
          id="mass"
          type="number"
          value={mass}
          onChange={(e) => setMass(e.target.value)}
          placeholder="Enter mass in kg"
          min="0.1"
          step="0.1"
        />
      </div>

      <div className="input-group">
        <label>Conversion Method</label>
        <div className="radio-group">
          {CONVERSION_METHODS.map((method) => (
            <label key={method} className="radio-label">
              <input
                type="radio"
                name="conversion-method"
                value={method}
                checked={conversionMethod === method}
                onChange={(e) => setConversionMethod(e.target.value)}
              />
              <span>{method}</span>
            </label>
          ))}
        </div>
      </div>

      <button className="run-button" onClick={onRunSimulation}>
        Run Simulation
      </button>
    </div>
  );
}

export default InputPanel;
