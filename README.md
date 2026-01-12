# 🟢Circleverses: Household Wealth Formation Simulation 🏡

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Python-based simulation system for analyzing household wealth formation patterns across different economic environments. Features a green wireframe aesthetic visualization matching classic vector graphics displays.

![cover](dev/circleverses2.png)

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Circlverses** | Towns represented as circular spatial layouts |
| **Cluster Cubes** | Households (like dice, positioned within Circlverses) |
| **Dots** | Household members (like dots on dice faces, 1-6 per household) |

## Features

| Feature | Description |
|---------|-------------|
| **Object-Oriented Design** | Clear class hierarchy with Dot, ClusterCube, Circlverse, and Simulation classes |
| **Economic Engine** | Monthly simulation cycles with income, expenses, and wealth accumulation |
| **Green Wireframe Visualization** | Aesthetic visualization matching classic vector graphics (index.js style) |
| **Multiple Scenarios** | Configure prosperous, struggling, or balanced economic environments |
| **Economic Shocks** | Simulate job loss, medical expenses, and windfalls |
| **Data Export** | Export simulation data to CSV for external analysis |
| **Interactive Controller** | Command-line interface for step-by-step simulation control |
| **Statistics & Analysis** | Gini coefficient, wealth distribution, and aggregate metrics |

## Installation

### Requirements

- Python 3.7 or higher
- matplotlib >= 3.5.0
- numpy >= 1.20.0

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install matplotlib numpy
```

## Quick Start

### Basic Example

```python
from setup import create_example_simulation
from visualization import visualize_simulation, print_statistics
import matplotlib.pyplot as plt

# Create example simulation (3 towns, 10-18 households each)
sim = create_example_simulation()

# Run for 12 months
sim.run_until(12)

# Print statistics
print_statistics(sim)

# Visualize
fig = visualize_simulation(sim)
plt.show()
```

### Run Examples

```bash
# Run all examples
python example.py

# Run specific example
python example.py 1  # Basic simulation
python example.py 2  # Step-by-step
python example.py 3  # Manual configuration
python example.py 4  # Economic shocks
python example.py 5  # Data export
```

### Interactive Controller

```bash
# Interactive mode
python controller.py

# Run for 12 months and then interactive
python controller.py --run 12

# Create custom simulation
python controller.py --random 2 15  # 2 towns, 15 households each

# Export data
python controller.py --run 24 --export data.csv

# Visualize
python controller.py --visualize
```

## Architecture

### Core Classes

| Class | Purpose | Key Attributes |
|-------|---------|----------------|
| **`Dot`** | Household member | Age, occupation type, working status, monthly income |
| **`ClusterCube`** | Household | ID, number of dots (1-6), location, wealth, savings rate, expenses, historical data |
| **`Circlverse`** | Town | Circular layout, economic multiplier, cost of living index, cluster cubes collection, statistics |
| **`CircleverseSimulation`** | Main controller | Multiple Circlverses, time tracking, pause/resume, data export, global statistics |

#### `Dot`

Represents a household member with age, occupation type, working status, and monthly income calculation.

#### `ClusterCube`

Represents a household with unique ID, number of members (dots: 1-6), financial attributes (wealth, savings rate, expenses), spatial location within a Circlverse, and historical tracking.

#### `Circlverse`

Represents a town with circular spatial layout, economic multiplier (prosperity level), cost of living index, collection of cluster cubes, and collective metrics/statistics.

#### `CircleverseSimulation`

Main simulation controller managing multiple Circlverses, time tracking, pause/resume functionality, data export, and global statistics.

### Configuration

#### Random Configuration

```python
from setup import create_random_circlverse

cv = create_random_circlverse(
    circlverse_id="MyTown",
    num_households=20,
    economic_multiplier=1.2,  # Prosperous
    cost_of_living_index=1.0  # Average
)
```

#### Manual Configuration

```python
from simulation import Circlverse, ClusterCube, Dot, OccupationType

cv = Circlverse("CustomTown", economic_multiplier=1.0, cost_of_living_index=1.0)

# Add specific household
dots = [
    Dot(age=35, occupation=OccupationType.PROFESSIONAL, is_working=True),
    Dot(age=32, occupation=OccupationType.PROFESSIONAL, is_working=True)
]
cube = ClusterCube(
    cube_id="HH001",
    num_dots=2,
    dots=dots,
    num_dependents=1,
    savings_rate=0.20
)
cv.add_cluster_cube(cube)
```

## Economic Simulation

### Monthly Cycle

Each month, for each household:

1. Calculate total income (sum of all working members)
2. Apply economic multiplier (local economic health)
3. Calculate expenses (housing, food, healthcare, etc.)
4. Apply cost of living index
5. Add random variation (±10%)
6. Calculate net income
7. Apply savings rate
8. Update wealth

### Economic Parameters

**Occupation Income (Monthly Base):**

| Occupation Type | Monthly Income |
|----------------|----------------|
| Professional | $8,000 |
| Skilled Trade | $5,000 |
| Service | $3,000 |
| Retail | $2,500 |
| Unemployed | $0 |

**Base Expenses (as fraction of income):**

| Category | Percentage | Notes |
|----------|-----------|-------|
| Housing | 35% | Plus per-person adjustment |
| Food | 15% | Plus per-person adjustment |
| Healthcare | 10% | Fixed percentage |
| Transportation | 10% | Fixed percentage |
| Utilities | 8% | Fixed percentage |
| Other | 22% | Miscellaneous expenses |

### Economic Shocks

```python
# Job loss
cube.apply_economic_shock("job_loss", 0)

# Medical expense
cube.apply_economic_shock("medical", -5000)

# Windfall
cube.apply_economic_shock("windfall", 10000)
```

## Visualization

The visualization uses a green wireframe aesthetic (`#50FF50` on `#101010` background):

| Visual Element | Representation |
|----------------|----------------|
| **Circles** | Circlverses (towns) - dashed circular boundaries |
| **Squares with dots** | Cluster Cubes (households) - dice-like representation |
| **Dot patterns** | Household size (1-6 dots, matching dice faces) |
| **Color intensity** | Wealth level (darker = lower, brighter = higher) |
| **Size** | Optionally scales with wealth (1x to 1.5x base size) |
| **Line styles** | Differentiated styles (solid, dashed, dash-dot) for time series |
| **Markers** | Unique markers (circle, square, X, triangle) for each Circlverse |

### Visualization Functions

```python
from visualization import visualize_simulation, plot_wealth_distribution

# Full simulation visualization
fig = visualize_simulation(sim, show_statistics=True)
plt.show()

# Wealth distribution histogram
fig, ax = plt.subplots(1, 1, facecolor="#101010")
plot_wealth_distribution(ax, sim)
plt.show()
```

## Data Export

Export simulation data to CSV:

```python
sim.export_to_csv("simulation_data.csv")
```

**CSV Columns:**

| Column | Description |
|--------|-------------|
| Month | Simulation month (0-indexed) |
| Circlverse_ID | Identifier of the town |
| Cube_ID | Identifier of the household |
| Wealth | Current wealth at end of month |
| Income | Total income for the month |
| Expenses | Total expenses for the month |
| Num_Dots | Number of household members (1-6) |
| Num_Dependents | Number of dependents (children, elderly) |
| Location_X | X coordinate within Circlverse |
| Location_Y | Y coordinate within Circlverse |

## Statistics

### Available Metrics

| Metric Category | Description |
|----------------|-------------|
| **Global Statistics** | Total households, average wealth, total wealth, wealth range across all Circlverses |
| **Per-Circlverse Statistics** | Individual town metrics (household count, average wealth, economic parameters) |
| **Wealth Distribution** | Min, max, mean, and median wealth values |
| **Gini Coefficient** | Inequality measure (0 = perfect equality, 1 = perfect inequality) |

```python
from visualization import print_statistics

print_statistics(sim)

# Or access programmatically
stats = sim.get_global_statistics()
gini = cv.calculate_gini_coefficient()
dist = cv.get_wealth_distribution()
```

## Customization

### Custom Occupation Types

Modify `simulation.py`:

```python
class OccupationType(Enum):
    # Add new types
    TECH = "tech"
    ARTIST = "artist"

OCCUPATION_INCOME[OccupationType.TECH] = 10000
OCCUPATION_INCOME[OccupationType.ARTIST] = 3000
```

### Custom Expense Categories

Modify `BASE_EXPENSES` in `simulation.py`:

```python
BASE_EXPENSES = {
    "housing": 0.35,
    "food": 0.15,
    # Add custom categories
    "education": 0.10,
    # ...
}
```

## Examples

See `example.py` for detailed examples:

| Example | Description | Command |
|---------|-------------|---------|
| **Basic Simulation** | Create and run example simulation | `python example.py 1` |
| **Step-by-Step** | Manual step control | `python example.py 2` |
| **Manual Configuration** | Custom household setup | `python example.py 3` |
| **Economic Shocks** | Applying shocks during simulation | `python example.py 4` |
| **Data Export** | Exporting to CSV | `python example.py 5` |

## File Structure

```
circleverse/
├── simulation.py      # Core classes and simulation engine
├── visualization.py   # Visualization functions (green wireframe)
├── setup.py          # Configuration and setup functions
├── controller.py       # Interactive command-line controller
├── example.py        # Usage examples
├── __init__.py       # Package initialization
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

| File | Purpose |
|------|---------|
| `simulation.py` | Core classes (Dot, ClusterCube, Circlverse, CircleverseSimulation) and economic engine |
| `visualization.py` | Green wireframe visualization functions and plotting |
| `setup.py` | Configuration helpers for creating simulations |
| `controller.py` | Interactive command-line controller for simulation control |
| `example.py` | 5 comprehensive usage examples |
| `__init__.py` | Package exports and initialization |
| `requirements.txt` | Python package dependencies (matplotlib, numpy) |

## License

This simulation is provided as-is for educational and research purposes.

## Future Enhancements

Potential improvements:

- Web-based visualization (HTML5 Canvas like index.js)
- Real-time interactive controls
- More complex economic models
- Network effects between households
- Migration between Circlverses
- Policy interventions
- More detailed demographic modeling
