"""
Graph generation for the PROMETHEUS Waste-to-Fuel Simulator.
This module handles all visualization of simulation results.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def create_energy_bar_chart(energy_required, energy_output):
    """
    Create a bar chart comparing energy required vs energy output.
    
    Args:
        energy_required (float): Energy required for conversion (kWh)
        energy_output (float): Energy output from produced fuels (kWh)
        
    Returns:
        matplotlib.figure.Figure: Figure object containing the bar chart
    """
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # Data for the bar chart
    categories = ['Energy Required', 'Energy Output']
    values = [energy_required, energy_output]
    
    # Create bars with different colors based on energy balance
    colors = ['#FF6B6B', '#4ECB71'] if energy_output > energy_required else ['#FF6B6B', '#FF9671']
    
    # Create the bar chart
    bars = ax.bar(categories, values, color=colors, width=0.4)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f} kWh',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    # Add labels and title
    ax.set_ylabel('Energy (kWh)')
    ax.set_title('Energy Balance')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust layout
    fig.tight_layout()
    
    return fig


def create_fuel_pie_chart(fuel_produced):
    """
    Create a pie chart showing distribution of fuel products.
    
    Args:
        fuel_produced (dict): Dictionary with fuel types as keys and produced amounts as values
        
    Returns:
        matplotlib.figure.Figure: Figure object containing the pie chart
    """
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # Filter out fuels with zero production
    fuel_produced = {k: v for k, v in fuel_produced.items() if v > 0}
    
    # Data for the pie chart
    labels = list(fuel_produced.keys())
    sizes = list(fuel_produced.values())
    
    # Calculate percentages for labels
    total = sum(sizes)
    percentages = [100 * s / total for s in sizes]
    
    # Create custom labels with percentages
    custom_labels = [f'{l} ({p:.1f}%)' for l, p in zip(labels, percentages)]
    
    # Create the pie chart with a colorful palette
    colors = plt.cm.Paired(np.linspace(0, 1, len(labels)))
    ax.pie(sizes, labels=custom_labels, autopct='', startangle=90, colors=colors)
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    
    # Add title
    ax.set_title('Fuel Product Distribution')
    
    # Adjust layout
    fig.tight_layout()
    
    return fig


def create_time_series_chart(time_data):
    """
    Create a line graph showing energy balance over time.
    
    Args:
        time_data (pandas.DataFrame): DataFrame with columns 'day', 'energy_required', 'energy_output', 'net_balance'
        
    Returns:
        matplotlib.figure.Figure: Figure object containing the line graph
    """
    fig = Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # Plot the data
    ax.plot(time_data['day'], time_data['energy_required'], label='Energy Required', color='#FF6B6B')
    ax.plot(time_data['day'], time_data['energy_output'], label='Energy Output', color='#4ECB71')
    ax.plot(time_data['day'], time_data['net_balance'], label='Net Balance', color='#3A86FF', linestyle='--')
    
    # Add a horizontal line at y=0 for reference
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    
    # Add labels and title
    ax.set_xlabel('Day')
    ax.set_ylabel('Energy (kWh)')
    ax.set_title('Energy Balance Over Time')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    
    # Adjust layout
    fig.tight_layout()
    
    return fig


def embed_figure_in_tkinter(figure, frame):
    """
    Embed a matplotlib figure in a tkinter frame.
    
    Args:
        figure (matplotlib.figure.Figure): Figure to embed
        frame (tkinter.Frame): Frame to embed the figure in
        
    Returns:
        FigureCanvasTkAgg: Canvas containing the embedded figure
    """
    canvas = FigureCanvasTkAgg(figure, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
    
    return canvas