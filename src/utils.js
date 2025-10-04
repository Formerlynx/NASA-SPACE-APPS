import { EFFICIENCY, FUEL_OUTPUT_FRACTIONS, ENERGY_INPUT, ENERGY_CONTENT } from './data';

export function calculateConversion(wasteType, mass, conversionMethod) {
  const efficiency = EFFICIENCY[wasteType][conversionMethod];
  const fuelFractions = FUEL_OUTPUT_FRACTIONS[wasteType][conversionMethod];
  const energyInputCost = ENERGY_INPUT[wasteType][conversionMethod];

  const energyRequired = mass * energyInputCost;

  const fuelProduced = {};
  for (const [fuelType, fraction] of Object.entries(fuelFractions)) {
    fuelProduced[fuelType] = mass * efficiency * fraction;
  }

  const fuelEnergyOutput = {};
  for (const [fuelType, fuelMass] of Object.entries(fuelProduced)) {
    fuelEnergyOutput[fuelType] = fuelMass * ENERGY_CONTENT[fuelType];
  }

  const totalEnergyOutput = Object.values(fuelEnergyOutput).reduce((sum, val) => sum + val, 0);
  const netEnergyBalance = totalEnergyOutput - energyRequired;
  const conversionEfficiency = energyRequired > 0 ? (totalEnergyOutput / energyRequired) * 100 : 0;

  return {
    wasteType,
    mass,
    conversionMethod,
    efficiency,
    energyRequired,
    fuelProduced,
    fuelEnergyOutput,
    totalEnergyOutput,
    netEnergyBalance,
    conversionEfficiency
  };
}

export function formatNumber(value, precision = 2) {
  return value.toFixed(precision);
}

export function formatEnergy(valueKwh, precision = 2) {
  return `${formatNumber(valueKwh, precision)} kWh`;
}

export function formatMass(valueKg, precision = 2) {
  return `${formatNumber(valueKg, precision)} kg`;
}

export function formatPercentage(value, precision = 1) {
  return `${formatNumber(value, precision)}%`;
}
