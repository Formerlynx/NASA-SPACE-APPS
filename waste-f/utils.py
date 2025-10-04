"""
Helper functions for the PROMETHEUS Waste-to-Fuel Simulator.
"""

def format_number(value, precision=2):
    """
    Format a number with the specified precision and add thousand separators.
    
    Args:
        value (float): The number to format
        precision (int): Number of decimal places
        
    Returns:
        str: Formatted number string
    """
    return f"{value:,.{precision}f}"


def format_energy(value_kwh, precision=2):
    """
    Format energy value with kWh unit.
    
    Args:
        value_kwh (float): Energy value in kWh
        precision (int): Number of decimal places
        
    Returns:
        str: Formatted energy string with unit
    """
    return f"{value_kwh:,.{precision}f} kWh"


def format_mass(value_kg, precision=2):
    """
    Format mass value with kg unit.
    
    Args:
        value_kg (float): Mass value in kg
        precision (int): Number of decimal places
        
    Returns:
        str: Formatted mass string with unit
    """
    return f"{value_kg:,.{precision}f} kg"


def format_percentage(value, precision=1):
    """
    Format a value as a percentage.
    
    Args:
        value (float): Value to format as percentage
        precision (int): Number of decimal places
        
    Returns:
        str: Formatted percentage string
    """
    return f"{value:,.{precision}f}%"


def create_summary_text(results):
    """
    Create a formatted text summary of simulation results.
    
    Args:
        results (dict): Dictionary containing simulation results
        
    Returns:
        str: Formatted summary text
    """
    summary = ["===== SIMULATION RESULTS ====="]
    
    # Add waste information
    summary.append(f"Waste Type: {results['waste_type']}")
    summary.append(f"Mass: {format_mass(results['mass'])}")
    summary.append(f"Conversion Method: {results['conversion_method']}")
    summary.append("")
    
    # Add fuel production information
    summary.append("FUEL PRODUCTION:")
    for fuel_type, amount in results['fuel_produced'].items():
        energy = results['fuel_energy_output'][fuel_type]
        summary.append(f"  {fuel_type.capitalize()}: {format_mass(amount)} ({format_energy(energy)})")
    summary.append("")
    
    # Add energy balance information
    summary.append("ENERGY BALANCE:")
    summary.append(f"  Energy Required: {format_energy(results['energy_required'])}")
    summary.append(f"  Energy Output: {format_energy(results['total_energy_output'])}")
    
    # Format net balance with + or - sign
    net_balance = results['net_energy_balance']
    sign = '+' if net_balance >= 0 else ''
    summary.append(f"  Net Balance: {sign}{format_energy(net_balance)}")
    summary.append(f"  Efficiency: {format_percentage(results['conversion_efficiency'])}")
    
    return "\n".join(summary)