"""
Constants and assumptions for the PROMETHEUS Waste-to-Fuel Simulator.
This file contains all the predefined constants used in the simulation.
"""

# Waste type constants
WASTE_TYPES = ["Plastic", "Organic", "Metal", "E-Waste"]

# Conversion method constants
CONVERSION_METHODS = ["Pyrolysis", "Plasma Gasification", "Anaerobic Digestion"]

# Efficiency by waste type and conversion method (0-1)
EFFICIENCY = {
    "Plastic": {
        "Pyrolysis": 0.65,
        "Plasma Gasification": 0.70,
        "Anaerobic Digestion": 0.30
    },
    "Organic": {
        "Pyrolysis": 0.55,
        "Plasma Gasification": 0.60,
        "Anaerobic Digestion": 0.75
    },
    "Metal": {
        "Pyrolysis": 0.20,
        "Plasma Gasification": 0.85,
        "Anaerobic Digestion": 0.10
    },
    "E-Waste": {
        "Pyrolysis": 0.45,
        "Plasma Gasification": 0.80,
        "Anaerobic Digestion": 0.15
    }
}

# Fuel output fractions by waste type and conversion method
FUEL_OUTPUT_FRACTIONS = {
    "Plastic": {
        "Pyrolysis": {"syngas": 0.6, "char": 0.3, "oil": 0.1},
        "Plasma Gasification": {"syngas": 0.7, "char": 0.3},
        "Anaerobic Digestion": {"methane": 0.8, "compost": 0.2}
    },
    "Organic": {
        "Pyrolysis": {"syngas": 0.5, "char": 0.4, "oil": 0.1},
        "Plasma Gasification": {"syngas": 0.65, "char": 0.35},
        "Anaerobic Digestion": {"methane": 0.9, "compost": 0.1}
    },
    "Metal": {
        "Pyrolysis": {"syngas": 0.3, "metal": 0.7},
        "Plasma Gasification": {"syngas": 0.6, "metal": 0.4},
        "Anaerobic Digestion": {"methane": 0.2, "metal": 0.8}
    },
    "E-Waste": {
        "Pyrolysis": {"syngas": 0.4, "char": 0.2, "metal": 0.4},
        "Plasma Gasification": {"syngas": 0.65, "metal": 0.35},
        "Anaerobic Digestion": {"methane": 0.3, "compost": 0.1, "metal": 0.6}
    }
}

# Energy input cost (kWh/kg) by waste type and conversion method
ENERGY_INPUT = {
    "Plastic": {
        "Pyrolysis": 0.5,
        "Plasma Gasification": 0.6,
        "Anaerobic Digestion": 0.2
    },
    "Organic": {
        "Pyrolysis": 0.4,
        "Plasma Gasification": 0.55,
        "Anaerobic Digestion": 0.15
    },
    "Metal": {
        "Pyrolysis": 0.7,
        "Plasma Gasification": 0.8,
        "Anaerobic Digestion": 0.3
    },
    "E-Waste": {
        "Pyrolysis": 0.6,
        "Plasma Gasification": 0.7,
        "Anaerobic Digestion": 0.25
    }
}

# Energy content per fuel type (kWh/kg)
ENERGY_CONTENT = {
    "syngas": 5.0,
    "char": 8.0,
    "oil": 11.0,
    "methane": 14.0,
    "compost": 0.5,
    "metal": 0.0  # Metals don't have energy content in this context
}