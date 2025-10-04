# PROMETHEUS Waste-to-Fuel Simulator

A scientific simulation tool that converts different types of waste into usable fuels and shows energy balances.

## Overview

The PROMETHEUS Waste-to-Fuel Simulator is a Python application that simulates the conversion of various waste types into usable fuels through different conversion methods. It calculates energy balances, fuel production, and conversion efficiency, providing both numerical results and visual representations.

## Features

- Simulate conversion of different waste types (Plastic, Organic, Metal, E-Waste)
- Choose from multiple conversion methods (Pyrolysis, Plasma Gasification, Anaerobic Digestion)
- Calculate energy required, energy output, and net energy balance
- Visualize results with interactive charts
- Optional time-series simulation over multiple days

## Project Structure

```
PROMETHEUS-WasteToFuel/
│
├── main.py             # Handles UI + program flow (requires external libraries)
├── converter.py        # Core calculations
├── visualizer.py       # Graph generation (requires matplotlib)
├── data.py             # Constants and assumptions
├── utils.py            # Helper functions
├── simple_demo.py      # Interactive text-based version (no external dependencies)
├── run_simulator.bat   # Easy launcher for Windows users
├── create_executable.bat # Creates standalone executable (Windows)
└── README.md           # Documentation
```

## Requirements

- Python 3.6 or higher
- Required libraries for full UI version:
  - tkinter
  - matplotlib
  - pandas
  - numpy

## Installation

1. Ensure you have Python installed on your system
2. Install the required libraries for the full UI version:

```bash
pip install matplotlib pandas numpy
```

*Note: tkinter usually comes with Python installation*

## Running the Application

### Easiest Method (Windows)
Simply double-click the `run_simulator.bat` file to launch the application. This batch file will automatically find a working Python installation on your system.

### Creating a Standalone Executable (Windows)
If you want to create a standalone executable that doesn't require Python:

1. Double-click the `create_executable.bat` file
2. Wait for the process to complete
3. Run the generated `PROMETHEUS_Simulator.exe` file

This creates a single executable file that can be shared with others who don't have Python installed.

### Full UI Version
To run the simulator with the complete UI (requires matplotlib, pandas, numpy), navigate to the project directory and execute:

```bash
python main.py
```

### Interactive Text Version
If you don't have all the required libraries installed, you can run the interactive text-based version which demonstrates the core functionality without external dependencies:

```bash
python simple_demo.py
```

## How to Use

1. Select a waste type from the dropdown menu
2. Enter the mass of waste in kilograms
3. Choose a conversion method using the radio buttons
4. Optionally, check "Include Time Simulation" to see results over time
5. Click "Run Simulation" to see the results

## Example Case

The application comes with a pre-configured example case:
- Waste Type: Plastic
- Mass: 200 kg
- Conversion Method: Plasma Gasification

Expected results:
- Fuel Produced: ~140 kg (syngas and char)
- Energy Required: ~120 kWh
- Energy Output: ~826 kWh
- Net Balance: +706 kWh
- Efficiency: ~688%

## License

This project is created for educational and demonstration purposes.

## Acknowledgments

This simulator was developed as a hackathon-style demo project inspired by NASA Space Apps challenges, focusing on waste management and energy recovery technologies.