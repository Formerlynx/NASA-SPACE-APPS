"""Graphical version of the PROMETHEUS Waste-to-Fuel Simulator.
This version uses Tkinter which comes with standard Python installations.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
from data import WASTE_TYPES, CONVERSION_METHODS, EFFICIENCY, FUEL_OUTPUT_FRACTIONS, ENERGY_INPUT, ENERGY_CONTENT

# Import calculation functions from simple_demo.py
from simple_demo import calculate_conversion, format_number, format_energy, format_mass, format_percentage

class SimpleCanvas(tk.Canvas):
    """A simple canvas for drawing charts without requiring matplotlib."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(bg="white")
    
    def clear(self):
        """Clear all drawings from the canvas."""
        self.delete("all")
    
    def draw_bar_chart(self, data, title="Bar Chart"):
        """Draw a simple bar chart.
        
        Args:
            data: Dictionary with labels as keys and values as values
            title: Title of the chart
        """
        self.clear()
        
        # Chart dimensions
        width = self.winfo_width()
        height = self.winfo_height()
        margin = 50
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        # Draw title
        self.create_text(width/2, margin/2, text=title, font=("Arial", 12, "bold"))
        
        # Calculate bar width and spacing
        num_bars = len(data)
        if num_bars == 0:
            return
            
        bar_width = min(60, chart_width / (num_bars * 2))
        spacing = bar_width / 2
        
        # Find maximum value for scaling
        max_value = max(abs(val) for val in data.values())
        if max_value == 0:
            max_value = 1  # Avoid division by zero
        
        # Draw bars
        x = margin + spacing
        for label, value in data.items():
            # Calculate bar height (scaled)
            bar_height = (abs(value) / max_value) * (chart_height - margin)
            
            # Determine bar color and position
            if value >= 0:
                y0 = height - margin - bar_height
                y1 = height - margin
                color = "#4CAF50"  # Green for positive
            else:
                y0 = height - margin
                y1 = height - margin + bar_height
                color = "#F44336"  # Red for negative
            
            # Draw bar
            self.create_rectangle(x, y0, x + bar_width, y1, fill=color)
            
            # Draw value
            value_text = f"{value:.1f}"
            if value >= 0:
                self.create_text(x + bar_width/2, y0 - 10, text=value_text)
            else:
                self.create_text(x + bar_width/2, y1 + 10, text=value_text)
            
            # Draw label (rotated for better fit)
            self.create_text(x + bar_width/2, height - margin/2, text=label, angle=45, anchor="e")
            
            x += bar_width + spacing
    
    def draw_pie_chart(self, data, title="Pie Chart"):
        """Draw a simple pie chart.
        
        Args:
            data: Dictionary with labels as keys and percentage values as values
            title: Title of the chart
        """
        self.clear()
        
        # Chart dimensions
        width = self.winfo_width()
        height = self.winfo_height()
        margin = 50
        
        # Calculate center and radius
        center_x = width / 2
        center_y = height / 2
        radius = min(center_x, center_y) - margin
        
        # Draw title
        self.create_text(width/2, margin/2, text=title, font=("Arial", 12, "bold"))
        
        # Colors for pie slices
        colors = ["#4CAF50", "#2196F3", "#FFC107", "#F44336", "#9C27B0", "#795548"]
        
        # Calculate total for percentages
        total = sum(data.values())
        if total == 0:
            return
        
        # Draw pie slices
        start_angle = 0
        legend_y = margin
        
        for i, (label, value) in enumerate(data.items()):
            # Calculate angles
            angle = (value / total) * 360
            end_angle = start_angle + angle
            
            # Draw slice
            color = colors[i % len(colors)]
            self.create_arc(center_x - radius, center_y - radius, 
                           center_x + radius, center_y + radius,
                           start=start_angle, extent=angle, 
                           fill=color, outline="white", width=2)
            
            # Calculate position for label inside pie
            mid_angle = math.radians(start_angle + angle/2)
            label_radius = radius * 0.7
            label_x = center_x + label_radius * math.cos(mid_angle)
            label_y = center_y + label_radius * math.sin(mid_angle)
            
            # Draw percentage in pie
            percentage = (value / total) * 100
            self.create_text(label_x, label_y, text=f"{percentage:.1f}%", fill="white", font=("Arial", 9, "bold"))
            
            # Draw legend item
            legend_x = width - margin - 100
            self.create_rectangle(legend_x, legend_y, legend_x + 15, legend_y + 15, fill=color)
            self.create_text(legend_x + 60, legend_y + 7, text=f"{label}: {percentage:.1f}%", anchor="w")
            legend_y += 20
            
            start_angle = end_angle

class WasteToFuelSimulator(tk.Tk):
    """Main application window for the Waste-to-Fuel Simulator."""
    
    def __init__(self):
        super().__init__()
        
        self.title("PROMETHEUS Waste-to-Fuel Simulator")
        self.geometry("800x600")
        self.minsize(800, 600)
        
        self.create_widgets()
        self.results = None
        
        # Run initial simulation with default values
        self.run_simulation()
    
    def create_widgets(self):
        """Create all UI widgets."""
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="PROMETHEUS Waste-to-Fuel Simulator", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Input frame (left side)
        input_frame = ttk.LabelFrame(main_frame, text="Input Parameters", padding="10")
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        # Waste type selection
        ttk.Label(input_frame, text="Waste Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.waste_type_var = tk.StringVar(value=WASTE_TYPES[0])
        waste_type_combo = ttk.Combobox(input_frame, textvariable=self.waste_type_var, 
                                      values=WASTE_TYPES, state="readonly")
        waste_type_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        waste_type_combo.bind("<<ComboboxSelected>>", lambda e: self.run_simulation())
        
        # Mass input
        ttk.Label(input_frame, text="Mass (kg):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.mass_var = tk.StringVar(value="200")
        mass_entry = ttk.Entry(input_frame, textvariable=self.mass_var, width=10)
        mass_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        mass_entry.bind("<Return>", lambda e: self.run_simulation())
        
        # Conversion method selection
        ttk.Label(input_frame, text="Conversion Method:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.conversion_method_var = tk.StringVar(value=CONVERSION_METHODS[0])
        
        # Create radio buttons for conversion methods
        for i, method in enumerate(CONVERSION_METHODS):
            rb = ttk.Radiobutton(input_frame, text=method, value=method, 
                               variable=self.conversion_method_var,
                               command=self.run_simulation)
            rb.grid(row=2+i, column=1, sticky=tk.W, pady=2)
        
        # Run button
        run_button = ttk.Button(input_frame, text="Run Simulation", command=self.run_simulation)
        run_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Output frame (right side)
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Results text area
        results_frame = ttk.LabelFrame(output_frame, text="Simulation Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=False)
        
        self.results_text = tk.Text(results_frame, height=10, width=50, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Charts frame
        charts_frame = ttk.LabelFrame(output_frame, text="Visualizations", padding="10")
        charts_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create tabs for different charts
        charts_notebook = ttk.Notebook(charts_frame)
        charts_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Energy balance chart tab
        energy_tab = ttk.Frame(charts_notebook)
        charts_notebook.add(energy_tab, text="Energy Balance")
        self.energy_canvas = SimpleCanvas(energy_tab, width=400, height=300)
        self.energy_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Fuel distribution chart tab
        fuel_tab = ttk.Frame(charts_notebook)
        charts_notebook.add(fuel_tab, text="Fuel Distribution")
        self.fuel_canvas = SimpleCanvas(fuel_tab, width=400, height=300)
        self.fuel_canvas.pack(fill=tk.BOTH, expand=True)
    
    def run_simulation(self):
        """Run the simulation with current input values."""
        try:
            # Get input values
            waste_type = self.waste_type_var.get()
            mass = float(self.mass_var.get())
            conversion_method = self.conversion_method_var.get()
            
            # Validate mass
            if mass <= 0:
                messagebox.showerror("Invalid Input", "Mass must be greater than zero.")
                return
            
            # Run calculation
            self.results = calculate_conversion(waste_type, mass, conversion_method)
            
            # Update results display
            self.update_results_display()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for mass.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_results_display(self):
        """Update the results display with current simulation results."""
        if not self.results:
            return
        
        # Update text results
        summary_text = self.create_formatted_summary()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, summary_text)
        
        # Update energy balance chart
        self.update_energy_chart()
        
        # Update fuel distribution chart
        self.update_fuel_chart()
    
    def create_formatted_summary(self):
        """Create a formatted text summary of the results."""
        r = self.results
        lines = []
        
        # Add waste information
        lines.append(f"Waste Type: {r['waste_type']}")
        lines.append(f"Mass: {format_mass(r['mass'])}")
        lines.append(f"Conversion Method: {r['conversion_method']}")
        lines.append("")
        
        # Add fuel production information
        lines.append("FUEL PRODUCTION:")
        for fuel_type, amount in r['fuel_produced'].items():
            energy = r['fuel_energy_output'][fuel_type]
            lines.append(f"  {fuel_type.capitalize()}: {format_mass(amount)} ({format_energy(energy)})")
        lines.append("")
        
        # Add energy balance information
        lines.append("ENERGY BALANCE:")
        lines.append(f"  Energy Required: {format_energy(r['energy_required'])}")
        lines.append(f"  Energy Output: {format_energy(r['total_energy_output'])}")
        
        # Format net balance with + or - sign
        net_balance = r['net_energy_balance']
        sign = '+' if net_balance >= 0 else ''
        lines.append(f"  Net Balance: {sign}{format_energy(net_balance)}")
        lines.append(f"  Efficiency: {format_percentage(r['conversion_efficiency'])}")
        
        return "\n".join(lines)
    
    def update_energy_chart(self):
        """Update the energy balance chart."""
        if not self.results:
            return
            
        # Prepare data for energy chart
        energy_data = {
            "Input": -self.results['energy_required'],  # Negative for visual clarity
            "Output": self.results['total_energy_output'],
            "Net": self.results['net_energy_balance']
        }
        
        # Draw the chart
        self.energy_canvas.draw_bar_chart(energy_data, "Energy Balance (kWh)")
    
    def update_fuel_chart(self):
        """Update the fuel distribution chart."""
        if not self.results:
            return
            
        # Prepare data for fuel distribution chart
        fuel_data = {}
        total_fuel = sum(self.results['fuel_produced'].values())
        
        if total_fuel > 0:
            for fuel_type, amount in self.results['fuel_produced'].items():
                percentage = (amount / total_fuel) * 100
                fuel_data[fuel_type.capitalize()] = percentage
        
        # Draw the chart
        self.fuel_canvas.draw_pie_chart(fuel_data, "Fuel Distribution (%)")

def main():
    """Run the application."""
    app = WasteToFuelSimulator()
    app.mainloop()

if __name__ == "__main__":
    main()