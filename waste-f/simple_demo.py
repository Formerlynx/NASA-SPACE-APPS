"""Simplified version of the PROMETHEUS Waste-to-Fuel Simulator.
This version doesn't require external libraries and demonstrates core functionality.
"""

from data import WASTE_TYPES, CONVERSION_METHODS, EFFICIENCY, FUEL_OUTPUT_FRACTIONS, ENERGY_INPUT, ENERGY_CONTENT

def calculate_conversion(waste_type, mass, conversion_method):
    """Calculate the waste-to-fuel conversion results."""
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

def format_number(value, precision=2):
    """Format a number with the specified precision."""
    return f"{value:.{precision}f}"

def format_energy(value_kwh, precision=2):
    """Format energy value with kWh unit."""
    return f"{value_kwh:.{precision}f} kWh"

def format_mass(value_kg, precision=2):
    """Format mass value with kg unit."""
    return f"{value_kg:.{precision}f} kg"

def format_percentage(value, precision=1):
    """Format a value as a percentage."""
    return f"{value:.{precision}f}%"

def create_summary_text(results):
    """Create a formatted text summary of simulation results."""
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

def display_menu(options, title="Select an option:"):
    """Display a menu of options and get user selection."""
    print(f"\n{title}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    while True:
        try:
            choice = int(input("Enter your choice (number): "))
            if 1 <= choice <= len(options):
                return options[choice-1]
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")

def get_numeric_input(prompt, min_value=0):
    """Get numeric input from user with validation."""
    while True:
        try:
            value = float(input(prompt))
            if value >= min_value:
                return value
            else:
                print(f"Please enter a value greater than or equal to {min_value}")
        except ValueError:
            print("Please enter a valid number")

def run_simulation(waste_type, mass, conversion_method):
    """Run the simulation and display results."""
    print(f"\nRunning simulation with:")
    print(f"  Waste Type: {waste_type}")
    print(f"  Mass: {mass} kg")
    print(f"  Conversion Method: {conversion_method}\n")
    
    # Calculate conversion
    results = calculate_conversion(waste_type, mass, conversion_method)
    
    # Display results
    summary = create_summary_text(results)
    print(summary)
    
    # Display fuel distribution as text-based chart
    print("\nFUEL DISTRIBUTION:")
    total_fuel = sum(results['fuel_produced'].values())
    for fuel_type, amount in results['fuel_produced'].items():
        percentage = (amount / total_fuel) * 100
        bar_length = int(percentage / 2)  # Scale to make bars reasonable length
        bar = '#' * bar_length
        print(f"  {fuel_type.capitalize()}: {format_percentage(percentage)} {bar}")

def main():
    """Run the interactive waste-to-fuel simulator."""
    print("\n" + "=" * 40)
    print("PROMETHEUS Waste-to-Fuel Simulator")
    print("=" * 40)
    print("\nWelcome to the PROMETHEUS Waste-to-Fuel Simulator!")
    print("This application demonstrates the conversion of various")
    print("waste types into useful fuels using different methods.")
    
    running = True
    while running:
        print("\n" + "-" * 40)
        print("MAIN MENU")
        print("-" * 40)
        
        # Get waste type
        waste_type = display_menu(WASTE_TYPES, "Select waste type:")
        
        # Get waste mass
        mass = get_numeric_input("Enter waste mass (kg): ", 0.1)
        
        # Get conversion method
        conversion_method = display_menu(CONVERSION_METHODS, "Select conversion method:")
        
        # Run simulation
        run_simulation(waste_type, mass, conversion_method)
        
        # Ask if user wants to run another simulation
        print("\n" + "-" * 40)
        choice = input("Run another simulation? (y/n): ").lower()
        if choice != 'y':
            running = False
    
    print("\nThank you for using PROMETHEUS Waste-to-Fuel Simulator!")
    print("Press Enter to exit...")
    input()

if __name__ == "__main__":
    main()