"""
Main module for the PROMETHEUS Waste-to-Fuel Simulator.
Handles UI and program flow.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np

# Import project modules
from data import WASTE_TYPES, CONVERSION_METHODS
from converter import calculate_conversion, simulate_over_time
from visualizer import create_energy_bar_chart, create_fuel_pie_chart, create_time_series_chart, embed_figure_in_tkinter
from utils import create_summary_text


class PrometheusApp:
    """
    Main application class for the PROMETHEUS Waste-to-Fuel Simulator.
    """
    def __init__(self, root):
        """
        Initialize the application.
        
        Args:
            root (tk.Tk): Root window
        """
        self.root = root
        self.root.title("PROMETHEUS Waste-to-Fuel Simulator")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Set theme colors
        self.bg_color = "#f5f5f5"
        self.accent_color = "#3a7ca5"
        self.root.configure(bg=self.bg_color)
        
        # Create main frames
        self.create_frames()
        
        # Create input panel
        self.create_input_panel()
        
        # Create output panel
        self.create_output_panel()
        
        # Initialize chart canvases
        self.energy_chart_canvas = None
        self.fuel_chart_canvas = None
        self.time_chart_canvas = None
        
        # Run a sample simulation for demo purposes
        self.run_sample_simulation()
    
    def create_frames(self):
        """
        Create the main frames for the application.
        """
        # Create main container frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create left panel for inputs
        self.left_frame = ttk.LabelFrame(self.main_frame, text="Simulation Inputs")
        self.left_frame.pack(side="left", fill="y", padx=5, pady=5)
        
        # Create right panel for outputs
        self.right_frame = ttk.LabelFrame(self.main_frame, text="Simulation Results")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Create frames for different output sections
        self.output_text_frame = ttk.Frame(self.right_frame)
        self.output_text_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.charts_frame = ttk.Frame(self.right_frame)
        self.charts_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create frames for charts
        self.top_charts_frame = ttk.Frame(self.charts_frame)
        self.top_charts_frame.pack(fill="x", padx=5, pady=5)
        
        self.energy_chart_frame = ttk.LabelFrame(self.top_charts_frame, text="Energy Balance")
        self.energy_chart_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        self.fuel_chart_frame = ttk.LabelFrame(self.top_charts_frame, text="Fuel Distribution")
        self.fuel_chart_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        self.time_chart_frame = ttk.LabelFrame(self.charts_frame, text="Simulation Over Time")
        self.time_chart_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    def create_input_panel(self):
        """
        Create the input panel with controls.
        """
        # Waste Type selection
        ttk.Label(self.left_frame, text="Waste Type:").pack(anchor="w", padx=10, pady=(10, 5))
        self.waste_type_var = tk.StringVar(value=WASTE_TYPES[0])
        waste_type_combo = ttk.Combobox(self.left_frame, textvariable=self.waste_type_var, values=WASTE_TYPES, state="readonly", width=20)
        waste_type_combo.pack(fill="x", padx=10, pady=(0, 10))
        
        # Mass input
        ttk.Label(self.left_frame, text="Mass (kg):").pack(anchor="w", padx=10, pady=(10, 5))
        self.mass_var = tk.StringVar(value="200")
        mass_entry = ttk.Entry(self.left_frame, textvariable=self.mass_var, width=20)
        mass_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Conversion Method selection
        ttk.Label(self.left_frame, text="Conversion Method:").pack(anchor="w", padx=10, pady=(10, 5))
        self.conversion_method_var = tk.StringVar(value=CONVERSION_METHODS[0])
        
        # Create radio buttons for conversion methods
        for method in CONVERSION_METHODS:
            ttk.Radiobutton(self.left_frame, text=method, variable=self.conversion_method_var, value=method).pack(anchor="w", padx=20, pady=2)
        
        # Add some space
        ttk.Separator(self.left_frame, orient="horizontal").pack(fill="x", padx=10, pady=15)
        
        # Run Simulation button
        run_button = ttk.Button(self.left_frame, text="Run Simulation", command=self.run_simulation)
        run_button.pack(fill="x", padx=10, pady=10)
        
        # Time simulation checkbox and entry
        self.time_sim_var = tk.BooleanVar(value=False)
        time_sim_check = ttk.Checkbutton(self.left_frame, text="Include Time Simulation", variable=self.time_sim_var)
        time_sim_check.pack(anchor="w", padx=10, pady=(10, 5))
        
        ttk.Label(self.left_frame, text="Days to Simulate:").pack(anchor="w", padx=10, pady=(5, 0))
        self.days_var = tk.StringVar(value="1000")
        days_entry = ttk.Entry(self.left_frame, textvariable=self.days_var, width=10)
        days_entry.pack(anchor="w", padx=10, pady=(0, 10))
    
    def create_output_panel(self):
        """
        Create the output panel for displaying results.
        """
        # Create text area for results
        self.results_text = scrolledtext.ScrolledText(self.output_text_frame, wrap=tk.WORD, height=15, width=50)
        self.results_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.results_text.config(font=("Consolas", 10))
    
    def run_simulation(self):
        """
        Run the simulation with the current input values.
        """
        try:
            # Get input values
            waste_type = self.waste_type_var.get()
            mass = float(self.mass_var.get())
            conversion_method = self.conversion_method_var.get()
            
            # Validate inputs
            if mass <= 0:
                raise ValueError("Mass must be greater than zero.")
            
            # Calculate conversion
            results = calculate_conversion(waste_type, mass, conversion_method)
            
            # Update text results
            summary_text = create_summary_text(results)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, summary_text)
            
            # Create and display charts
            self.update_charts(results)
            
            # Run time simulation if selected
            if self.time_sim_var.get():
                try:
                    days = int(self.days_var.get())
                    if days <= 0:
                        raise ValueError("Days must be greater than zero.")
                    
                    # Run time simulation
                    time_data = simulate_over_time(waste_type, mass/365, conversion_method, days)
                    
                    # Create and display time chart
                    self.update_time_chart(time_data)
                except ValueError as e:
                    self.results_text.insert(tk.END, f"\n\nError in time simulation: {str(e)}")
            
        except ValueError as e:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Error: {str(e)}\n\nPlease check your inputs and try again.")
        except Exception as e:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"An unexpected error occurred: {str(e)}\n\nPlease check your inputs and try again.")
    
    def update_charts(self, results):
        """
        Update the charts with new simulation results.
        
        Args:
            results (dict): Dictionary containing simulation results
        """
        # Clear existing charts if they exist
        if self.energy_chart_canvas:
            self.energy_chart_canvas.get_tk_widget().destroy()
        
        if self.fuel_chart_canvas:
            self.fuel_chart_canvas.get_tk_widget().destroy()
        
        # Create energy balance bar chart
        energy_fig = create_energy_bar_chart(results['energy_required'], results['total_energy_output'])
        self.energy_chart_canvas = embed_figure_in_tkinter(energy_fig, self.energy_chart_frame)
        
        # Create fuel distribution pie chart
        fuel_fig = create_fuel_pie_chart(results['fuel_produced'])
        self.fuel_chart_canvas = embed_figure_in_tkinter(fuel_fig, self.fuel_chart_frame)
    
    def update_time_chart(self, time_data):
        """
        Update the time series chart with simulation data.
        
        Args:
            time_data (pandas.DataFrame): DataFrame with time simulation results
        """
        # Clear existing time chart if it exists
        if self.time_chart_canvas:
            self.time_chart_canvas.get_tk_widget().destroy()
        
        # Create time series chart
        time_fig = create_time_series_chart(time_data)
        self.time_chart_canvas = embed_figure_in_tkinter(time_fig, self.time_chart_frame)
    
    def run_sample_simulation(self):
        """
        Run a sample simulation for demo purposes.
        Uses the example case from the requirements.
        """
        # Set input values to match example case
        self.waste_type_var.set("Plastic")
        self.mass_var.set("200")
        self.conversion_method_var.set("Plasma Gasification")
        
        # Run the simulation
        self.run_simulation()


def main():
    """
    Main function to start the application.
    """
    root = tk.Tk()
    app = PrometheusApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()