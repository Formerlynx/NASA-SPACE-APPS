"""
Core calculations for the PROMETHEUS Waste-to-Fuel Simulator.
This module handles all the conversion calculations from waste to fuel.
"""

import pandas as pd
import numpy as np
from data import EFFICIENCY, FUEL_OUTPUT_FRACTIONS, ENERGY_INPUT, ENERGY_CONTENT


def calculate_conversion(waste_type, mass, conversion_method):
    """
    Calculate the waste-to-fuel conversion results.
    
    Args:
        waste_type (str): Type of waste (Plastic, Organic, Metal, E-Waste)
        mass (float): Mass of waste in kg
        conversion_method (str): Method of conversion (Pyrolysis, Plasma Gasification, Anaerobic Digestion)
        
    Returns:
        dict: Dictionary containing all calculation results
    """
    # Get efficiency for the given waste type and conversion method
    efficiency = EFFICIENCY[waste_type][conversion_method]
    
    # Get fuel output fractions
    fuel_fractions = FUEL_OUTPUT_FRACTIONS[waste_type][conversion_method]
    
    # Get energy input cost
    energy_input_cost = ENERGY_INPUT[waste_type][conversion_method]
    
    # Calculate energy required
    energy_required = mass * energy_input_cost
    
    # Calculate fuel produced for each fuel type
    fuel_produced = {}
    for fuel_type, fraction in fuel_fractions.items():
        fuel_produced[fuel_type] = mass * efficiency * fraction
    
    # Calculate energy output for each fuel type
    fuel_energy_output = {}
    for fuel_type, fuel_mass in fuel_produced.items():
        fuel_energy_output[fuel_type] = fuel_mass * ENERGY_CONTENT[fuel_type]
    
    # Calculate total energy output
    total_energy_output = sum(fuel_energy_output.values())
    
    # Calculate net energy balance
    net_energy_balance = total_energy_output - energy_required
    
    # Calculate conversion efficiency percentage
    # Avoid division by zero
    if energy_required > 0:
        conversion_efficiency = (total_energy_output / energy_required) * 100
    else:
        conversion_efficiency = 0
    
    # Prepare results
    results = {
        "waste_type": waste_type,
        "mass": mass,
        "conversion_method": conversion_method,
        "efficiency": efficiency,
        "energy_required": energy_required,
        "fuel_produced": fuel_produced,
        "fuel_energy_output": fuel_energy_output,
        "total_energy_output": total_energy_output,
        "net_energy_balance": net_energy_balance,
        "conversion_efficiency": conversion_efficiency
    }
    
    return results


def simulate_over_time(waste_type, daily_mass, conversion_method, days=1000):
    """
    Simulate waste conversion over a period of time.
    
    Args:
        waste_type (str): Type of waste
        daily_mass (float): Daily mass of waste in kg
        conversion_method (str): Method of conversion
        days (int): Number of days to simulate
        
    Returns:
        pandas.DataFrame: DataFrame with daily results
    """
    # Create empty DataFrame to store results
    columns = ['day', 'energy_required', 'energy_output', 'net_balance']
    df = pd.DataFrame(columns=columns)
    
    # Simulate for each day
    for day in range(1, days + 1):
        # Add some random variation to daily waste (±10%)
        daily_variation = np.random.uniform(0.9, 1.1)
        daily_waste = daily_mass * daily_variation
        
        # Calculate conversion for the day
        result = calculate_conversion(waste_type, daily_waste, conversion_method)
        
        # Add to DataFrame
        new_row = {
            'day': day,
            'energy_required': result['energy_required'],
            'energy_output': result['total_energy_output'],
            'net_balance': result['net_energy_balance']
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    return df