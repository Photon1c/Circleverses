"""
Circleverse Example Usage
Demonstrates how to create and run simulations
"""

from simulation import CircleverseSimulation, ClusterCube
from setup import create_example_simulation, create_random_circlverse
from visualization import visualize_simulation, print_statistics
import matplotlib.pyplot as plt


def example_basic_simulation():
    """Basic example: create and run a simple simulation"""
    print("="*60)
    print("EXAMPLE 1: Basic Simulation")
    print("="*60)
    
    # Create example simulation
    sim = create_example_simulation()
    
    # Run simulation for 12 months
    print("\nRunning simulation for 12 months...")
    sim.run_until(12)
    
    # Print statistics
    print_statistics(sim)
    
    # Visualize
    fig = visualize_simulation(sim)
    plt.show()


def example_step_by_step():
    """Example: Step through simulation month by month"""
    print("="*60)
    print("EXAMPLE 2: Step-by-Step Simulation")
    print("="*60)
    
    # Create a single circlverse
    cv = create_random_circlverse("Demo", num_households=10)
    sim = CircleverseSimulation()
    sim.add_circlverse(cv)
    
    # Run for 6 months, printing after each month
    for month in range(6):
        sim.step(1)
        stats = sim.get_global_statistics()
        print(f"Month {month + 1}: Average Wealth = ${stats['global_avg_wealth']:,.2f}")
    
    print_statistics(sim)


def example_manual_configuration():
    """Example: Manually configure households"""
    print("="*60)
    print("EXAMPLE 3: Manual Configuration")
    print("="*60)
    
    from simulation import Circlverse, ClusterCube, Dot, OccupationType
    
    # Create a circlverse manually
    cv = Circlverse(
        circlverse_id="Custom",
        radius=80.0,
        economic_multiplier=1.2,
        cost_of_living_index=0.9
    )
    
    # Add specific households
    # Household 1: Professional couple
    dots1 = [
        Dot(age=35, occupation=OccupationType.PROFESSIONAL, is_working=True),
        Dot(age=32, occupation=OccupationType.PROFESSIONAL, is_working=True)
    ]
    cube1 = ClusterCube(
        cube_id="Custom_HH001",
        num_dots=2,
        dots=dots1,
        num_dependents=1,
        savings_rate=0.20
    )
    cv.add_cluster_cube(cube1)
    
    # Household 2: Service worker with family
    dots2 = [
        Dot(age=28, occupation=OccupationType.SERVICE, is_working=True),
        Dot(age=26, occupation=OccupationType.RETAIL, is_working=True)
    ]
    cube2 = ClusterCube(
        cube_id="Custom_HH002",
        num_dots=2,
        dots=dots2,
        num_dependents=2,
        savings_rate=0.10
    )
    cv.add_cluster_cube(cube2)
    
    # Household 3: Single unemployed
    dots3 = [
        Dot(age=45, occupation=OccupationType.UNEMPLOYED, is_working=False)
    ]
    cube3 = ClusterCube(
        cube_id="Custom_HH003",
        num_dots=1,
        dots=dots3,
        savings_rate=0.0
    )
    cv.add_cluster_cube(cube3)
    
    # Run simulation
    sim = CircleverseSimulation()
    sim.add_circlverse(cv)
    
    print("\nRunning custom simulation for 24 months...")
    sim.run_until(24)
    
    print_statistics(sim)
    
    # Visualize
    fig = visualize_simulation(sim, show_statistics=False)
    plt.show()


def example_with_economic_shocks():
    """Example: Apply economic shocks to households"""
    print("="*60)
    print("EXAMPLE 4: Economic Shocks")
    print("="*60)
    
    sim = create_example_simulation()
    
    # Run for 6 months normally
    print("\nRunning normally for 6 months...")
    sim.run_until(6)
    stats_before = sim.get_global_statistics()
    print(f"Average wealth before shocks: ${stats_before['global_avg_wealth']:,.2f}")
    
    # Apply shocks
    print("\nApplying economic shocks...")
    for cv in sim.circlverses:
        # Random job loss
        if cv.cluster_cubes:
            cube = cv.cluster_cubes[0]
            cube.apply_economic_shock("job_loss", 0)
            print(f"  Applied job loss to {cube.cube_id}")
        
        # Medical expense
        if len(cv.cluster_cubes) > 1:
            cube = cv.cluster_cubes[1]
            cube.apply_economic_shock("medical", -5000)
            print(f"  Applied medical expense (-$5000) to {cube.cube_id}")
        
        # Windfall
        if len(cv.cluster_cubes) > 2:
            cube = cv.cluster_cubes[2]
            cube.apply_economic_shock("windfall", 10000)
            print(f"  Applied windfall (+$10000) to {cube.cube_id}")
    
    # Continue simulation
    print("\nContinuing simulation for 6 more months...")
    sim.run_until(12)
    
    stats_after = sim.get_global_statistics()
    print(f"Average wealth after shocks: ${stats_after['global_avg_wealth']:,.2f}")
    
    print_statistics(sim)


def example_export_data():
    """Example: Export simulation data to CSV"""
    print("="*60)
    print("EXAMPLE 5: Data Export")
    print("="*60)
    
    sim = create_example_simulation()
    sim.run_until(12)
    
    # Export to CSV
    filename = "circleverse_export.csv"
    sim.export_to_csv(filename)
    print(f"\nSimulation data exported to {filename}")
    print(f"Total months: {sim.current_month}")
    print(f"Total households: {sim.get_global_statistics()['total_households']}")


if __name__ == "__main__":
    import sys
    
    # Run specific example or all
    if len(sys.argv) > 1:
        example_num = int(sys.argv[1])
        examples = {
            1: example_basic_simulation,
            2: example_step_by_step,
            3: example_manual_configuration,
            4: example_with_economic_shocks,
            5: example_export_data
        }
        if example_num in examples:
            examples[example_num]()
        else:
            print(f"Example {example_num} not found. Available: 1-5")
    else:
        # Run all examples
        print("Running all examples...\n")
        
        # Example 1: Basic
        example_basic_simulation()
        
        # Example 2: Step by step
        print("\n\n")
        example_step_by_step()
        
        # Example 5: Export (non-visual)
        print("\n\n")
        example_export_data()
        
        print("\n\nTo see examples 3 and 4, run:")
        print("  python example.py 3  # Manual configuration")
        print("  python example.py 4  # Economic shocks")
