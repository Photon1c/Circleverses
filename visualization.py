"""
Circleverse Visualization Module
Green wireframe aesthetic matching the index.js style
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle
import numpy as np
from typing import List, Dict
import math

from simulation import Circlverse, ClusterCube, CircleverseSimulation

# Color scheme matching index.js
BACKGROUND_COLOR = "#101010"  # Dark background
FOREGROUND_COLOR = "#50FF50"  # Bright green wireframe


def draw_dice_face(ax, center_x: float, center_y: float, size: float, num_dots: int, 
                   color: str = FOREGROUND_COLOR, linewidth: float = 1.5):
    """
    Draw a dice face representation of a cluster cube
    Dots are positioned like on a real die (1-6 dots)
    """
    # Draw cube outline (square)
    square = Rectangle(
        (center_x - size/2, center_y - size/2), 
        size, size,
        fill=False,
        edgecolor=color,
        linewidth=linewidth
    )
    ax.add_patch(square)
    
    # Dot positions for dice faces (normalized to -0.3 to 0.3)
    dot_patterns = {
        1: [(0, 0)],
        2: [(-0.2, -0.2), (0.2, 0.2)],
        3: [(-0.2, -0.2), (0, 0), (0.2, 0.2)],
        4: [(-0.2, -0.2), (-0.2, 0.2), (0.2, -0.2), (0.2, 0.2)],
        5: [(-0.2, -0.2), (-0.2, 0.2), (0, 0), (0.2, -0.2), (0.2, 0.2)],
        6: [(-0.2, -0.25), (-0.2, 0), (-0.2, 0.25), (0.2, -0.25), (0.2, 0), (0.2, 0.25)]
    }
    
    pattern = dot_patterns.get(min(num_dots, 6), dot_patterns[6])
    dot_radius = size * 0.08
    
    for dx, dy in pattern:
        dot = Circle(
            (center_x + dx * size, center_y + dy * size),
            dot_radius,
            fill=True,
            facecolor=color,
            edgecolor=color,
            linewidth=linewidth * 0.5
        )
        ax.add_patch(dot)


def visualize_circlverse(ax, circlverse: Circlverse, wealth_color_scale: bool = True,
                         title: str = None):
    """
    Visualize a single Circlverse with its cluster cubes
    
    Args:
        ax: Matplotlib axes
        circlverse: Circlverse to visualize
        wealth_color_scale: If True, use color intensity for wealth
        title: Optional title for the subplot
    """
    # Draw the circle boundary (wireframe)
    circle = Circle(
        (0, 0), 
        circlverse.radius,
        fill=False,
        edgecolor=FOREGROUND_COLOR,
        linewidth=2,
        linestyle='--'
    )
    ax.add_patch(circle)
    
    # Get wealth range for color scaling
    if wealth_color_scale and circlverse.cluster_cubes:
        wealths = [cube.current_wealth for cube in circlverse.cluster_cubes]
        min_wealth = min(wealths)
        max_wealth = max(wealths)
        wealth_range = max_wealth - min_wealth if max_wealth > min_wealth else 1.0
    else:
        min_wealth = max_wealth = 0
        wealth_range = 1.0
    
    # Draw each cluster cube
    for cube in circlverse.cluster_cubes:
        x, y = cube.location
        
        # Calculate cube size based on wealth (optional)
        base_size = 8.0
        if wealth_color_scale and wealth_range > 0:
            wealth_factor = (cube.current_wealth - min_wealth) / wealth_range
            cube_size = base_size * (1.0 + wealth_factor * 0.5)  # 1x to 1.5x size
        else:
            cube_size = base_size
        
        # Calculate color intensity based on wealth
        if wealth_color_scale and wealth_range > 0:
            wealth_normalized = (cube.current_wealth - min_wealth) / wealth_range
            # Adjust brightness: 0.3 to 1.0 intensity
            color_intensity = 0.3 + wealth_normalized * 0.7
            # Convert hex to RGB, adjust, and convert back
            r = int(FOREGROUND_COLOR[1:3], 16)
            g = int(FOREGROUND_COLOR[3:5], 16)
            b = int(FOREGROUND_COLOR[5:7], 16)
            r_new = min(255, int(r * color_intensity))
            g_new = min(255, int(g * color_intensity))
            b_new = min(255, int(b * color_intensity))
            color_hex = f"#{r_new:02x}{g_new:02x}{b_new:02x}"
        else:
            color_hex = FOREGROUND_COLOR
        
        # Draw the dice face
        draw_dice_face(ax, x, y, cube_size, cube.num_dots, color=color_hex)
    
    # Set axis properties
    ax.set_aspect('equal')
    ax.set_facecolor(BACKGROUND_COLOR)
    ax.spines['top'].set_color(FOREGROUND_COLOR)
    ax.spines['bottom'].set_color(FOREGROUND_COLOR)
    ax.spines['left'].set_color(FOREGROUND_COLOR)
    ax.spines['right'].set_color(FOREGROUND_COLOR)
    ax.tick_params(colors=FOREGROUND_COLOR)
    ax.xaxis.label.set_color(FOREGROUND_COLOR)
    ax.yaxis.label.set_color(FOREGROUND_COLOR)
    
    # Set limits with padding
    padding = circlverse.radius * 0.2
    ax.set_xlim(-circlverse.radius - padding, circlverse.radius + padding)
    ax.set_ylim(-circlverse.radius - padding, circlverse.radius + padding)
    
    # Add axis labels to clarify spatial coordinates
    ax.set_xlabel("X Position", color=FOREGROUND_COLOR, fontsize=9, labelpad=6)
    ax.set_ylabel("Y Position", color=FOREGROUND_COLOR, fontsize=9, labelpad=6)
    
    if title:
        ax.set_title(title, color=FOREGROUND_COLOR, fontsize=10, pad=12, fontweight='normal')


def visualize_simulation(simulation: CircleverseSimulation, 
                        figsize: tuple = (14, 9),
                        show_statistics: bool = True):
    """
    Create a comprehensive visualization of the entire simulation
    
    Args:
        simulation: CircleverseSimulation instance
        figsize: Figure size (width, height)
        show_statistics: If True, show statistics panels
    """
    num_circlverses = len(simulation.circlverses)
    
    if show_statistics:
        # Create grid: 2 rows, top row for stats, bottom for circles
        # Increased hspace for better separation
        fig = plt.figure(figsize=figsize, facecolor=BACKGROUND_COLOR)
        gs = fig.add_gridspec(2, max(num_circlverses, 2), hspace=0.35, wspace=0.3, 
                              height_ratios=[1.2, 1])  # Give more space to top plot
        
        # Top row: Statistics plots
        if num_circlverses > 0:
            ax_wealth = fig.add_subplot(gs[0, :])
            plot_wealth_over_time(ax_wealth, simulation)
        
        # Bottom row: Circlverses
        axes = []
        for i, cv in enumerate(simulation.circlverses):
            ax = fig.add_subplot(gs[1, i])
            title = f"{cv.circlverse_id}\n(Econ: {cv.economic_multiplier:.2f}, COL: {cv.cost_of_living_index:.2f})"
            visualize_circlverse(ax, cv, title=title)
            axes.append(ax)
    else:
        # Simple grid of circlverses
        cols = min(3, num_circlverses)
        rows = (num_circlverses + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=figsize, facecolor=BACKGROUND_COLOR)
        if num_circlverses == 1:
            axes = [axes]
        elif rows == 1:
            axes = axes if isinstance(axes, list) else [axes]
        else:
            axes = axes.flatten()
        
        for i, cv in enumerate(simulation.circlverses):
            title = f"{cv.circlverse_id}"
            visualize_circlverse(axes[i], cv, title=title)
    
    fig.suptitle(
        f"Circleverse Simulation - Month {simulation.current_month}",
        color=FOREGROUND_COLOR,
        fontsize=14,
        fontweight='bold',
        y=0.98  # Position slightly lower to avoid overlap
    )
    
    # Ensure tight layout to prevent overlap
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    
    return fig


def plot_wealth_over_time(ax, simulation: CircleverseSimulation):
    """Plot wealth over time for all circlverses"""
    ax.set_facecolor(BACKGROUND_COLOR)
    ax.spines['top'].set_color(FOREGROUND_COLOR)
    ax.spines['bottom'].set_color(FOREGROUND_COLOR)
    ax.spines['left'].set_color(FOREGROUND_COLOR)
    ax.spines['right'].set_color(FOREGROUND_COLOR)
    ax.tick_params(colors=FOREGROUND_COLOR)
    ax.xaxis.label.set_color(FOREGROUND_COLOR)
    ax.yaxis.label.set_color(FOREGROUND_COLOR)
    
    # Define line styles and markers for differentiation
    line_styles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1))]  # solid, dashed, dashdot, dotted, custom
    markers = ['o', 's', '^', 'X', 'D', 'v', 'p', '*']  # circle, square, triangle, X, diamond, etc.
    marker_styles = ['', 'o', 's', 'X', '^', 'D']  # Mix of none and markers
    
    for idx, cv in enumerate(simulation.circlverses):
        if cv.wealth_history:
            months = list(range(len(cv.wealth_history)))
            linestyle = line_styles[idx % len(line_styles)]
            marker = markers[idx % len(markers)]
            # Use markers every Nth point to avoid clutter (every 3rd point)
            marker_every = max(1, len(months) // 20) if len(months) > 20 else 1
            
            ax.plot(months, cv.wealth_history, 
                   color=FOREGROUND_COLOR, 
                   linewidth=2.0,  # Slightly thicker for better visibility
                   linestyle=linestyle,
                   marker=marker,
                   markersize=5,
                   markevery=marker_every,
                   markerfacecolor=FOREGROUND_COLOR,
                   markeredgecolor=FOREGROUND_COLOR,
                   markeredgewidth=1,
                   label=f"{cv.circlverse_id}",
                   alpha=0.9)
    
    # Increase padding to avoid overlap with title and labels
    ax.set_xlabel("Month", color=FOREGROUND_COLOR, fontsize=11, labelpad=8)
    ax.set_ylabel("Average Wealth ($)", color=FOREGROUND_COLOR, fontsize=11, labelpad=8)
    ax.set_title("Average Wealth Over Time", color=FOREGROUND_COLOR, fontsize=12, pad=15, fontweight='bold')
    
    # Improve legend positioning and styling
    ax.legend(loc='upper left', facecolor=BACKGROUND_COLOR, edgecolor=FOREGROUND_COLOR,
              labelcolor=FOREGROUND_COLOR, framealpha=0.9, fontsize=9, 
              borderpad=0.5, labelspacing=0.5)
    
    # Improve grid
    ax.grid(True, color=FOREGROUND_COLOR, alpha=0.15, linestyle='--', linewidth=0.8)
    
    # Adjust tick parameters for better readability
    ax.tick_params(axis='both', which='major', labelsize=9)


def plot_wealth_distribution(ax, simulation: CircleverseSimulation):
    """Plot wealth distribution histogram"""
    ax.set_facecolor(BACKGROUND_COLOR)
    ax.spines['top'].set_color(FOREGROUND_COLOR)
    ax.spines['bottom'].set_color(FOREGROUND_COLOR)
    ax.spines['left'].set_color(FOREGROUND_COLOR)
    ax.spines['right'].set_color(FOREGROUND_COLOR)
    ax.tick_params(colors=FOREGROUND_COLOR)
    ax.xaxis.label.set_color(FOREGROUND_COLOR)
    ax.yaxis.label.set_color(FOREGROUND_COLOR)
    
    all_wealths = []
    for cv in simulation.circlverses:
        for cube in cv.cluster_cubes:
            all_wealths.append(cube.current_wealth)
    
    if all_wealths:
        ax.hist(all_wealths, bins=20, color=FOREGROUND_COLOR, alpha=0.5, 
               edgecolor=FOREGROUND_COLOR, linewidth=1)
        ax.set_xlabel("Wealth ($)", color=FOREGROUND_COLOR, fontsize=11, labelpad=8)
        ax.set_ylabel("Number of Households", color=FOREGROUND_COLOR, fontsize=11, labelpad=8)
        ax.set_title("Wealth Distribution", color=FOREGROUND_COLOR, fontsize=12, pad=15, fontweight='bold')
        ax.grid(True, color=FOREGROUND_COLOR, alpha=0.2, linestyle='--', axis='y')


def print_statistics(simulation: CircleverseSimulation):
    """Print formatted statistics to console"""
    print("\n" + "="*60)
    print(f"CIRCLEVERSE SIMULATION STATISTICS - Month {simulation.current_month}")
    print("="*60)
    
    global_stats = simulation.get_global_statistics()
    print(f"\nGlobal Statistics:")
    print(f"  Total Households: {global_stats.get('total_households', 0)}")
    print(f"  Total Circlverses: {global_stats.get('total_circlverses', 0)}")
    print(f"  Global Average Wealth: ${global_stats.get('global_avg_wealth', 0):,.2f}")
    print(f"  Global Total Wealth: ${global_stats.get('global_total_wealth', 0):,.2f}")
    print(f"  Wealth Range: ${global_stats.get('global_min_wealth', 0):,.2f} to ${global_stats.get('global_max_wealth', 0):,.2f}")
    
    for cv in simulation.circlverses:
        print(f"\n{cv.circlverse_id}:")
        print(f"  Households: {len(cv.cluster_cubes)}")
        print(f"  Economic Multiplier: {cv.economic_multiplier:.2f}")
        print(f"  Cost of Living: {cv.cost_of_living_index:.2f}")
        
        dist = cv.get_wealth_distribution()
        if dist:
            print(f"  Average Wealth: ${dist['mean']:,.2f}")
            print(f"  Median Wealth: ${dist['median']:,.2f}")
            print(f"  Wealth Range: ${dist['min']:,.2f} to ${dist['max']:,.2f}")
        
        gini = cv.calculate_gini_coefficient()
        print(f"  Gini Coefficient: {gini:.3f} ({'High inequality' if gini > 0.5 else 'Moderate inequality' if gini > 0.3 else 'Low inequality'})")
    
    print("="*60 + "\n")
