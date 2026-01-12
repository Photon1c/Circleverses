"""
Circleverse: Household Wealth Formation Simulation

A Python-based simulation system for analyzing household wealth formation
patterns across different economic environments.
"""

from simulation import (
    CircleverseSimulation,
    Circlverse,
    ClusterCube,
    Dot,
    OccupationType
)

from setup import (
    create_example_simulation,
    create_random_circlverse,
    create_manual_circlverse,
    create_simulation_from_config
)

from visualization import (
    visualize_simulation,
    visualize_circlverse,
    plot_wealth_over_time,
    plot_wealth_distribution,
    print_statistics
)

__version__ = "1.0.0"
__all__ = [
    "CircleverseSimulation",
    "Circlverse",
    "ClusterCube",
    "Dot",
    "OccupationType",
    "create_example_simulation",
    "create_random_circlverse",
    "create_manual_circlverse",
    "create_simulation_from_config",
    "visualize_simulation",
    "visualize_circlverse",
    "plot_wealth_over_time",
    "plot_wealth_distribution",
    "print_statistics",
]
