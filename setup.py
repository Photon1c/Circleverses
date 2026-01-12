"""
Circleverse Setup and Configuration Interface
Provides functions to create and configure simulations
"""

import random
from typing import List, Dict, Optional, Tuple
from simulation import (
    Circlverse, ClusterCube, CircleverseSimulation,
    OccupationType, Dot
)


def create_random_circlverse(
    circlverse_id: str,
    num_households: int,
    radius: float = 100.0,
    economic_multiplier: Optional[float] = None,
    cost_of_living_index: Optional[float] = None
) -> Circlverse:
    """
    Create a Circlverse with random household configurations
    
    Args:
        circlverse_id: Unique identifier
        num_households: Number of cluster cubes (households)
        radius: Radius of the circular town
        economic_multiplier: Economic health (default: random 0.7-1.3)
        cost_of_living_index: Cost multiplier (default: random 0.8-1.4)
    """
    if economic_multiplier is None:
        economic_multiplier = random.uniform(0.7, 1.3)
    if cost_of_living_index is None:
        cost_of_living_index = random.uniform(0.8, 1.4)
    
    cv = Circlverse(
        circlverse_id=circlverse_id,
        radius=radius,
        economic_multiplier=economic_multiplier,
        cost_of_living_index=cost_of_living_index
    )
    
    # Create random households
    for i in range(num_households):
        num_dots = random.randint(1, 6)  # Like dice: 1-6 members
        num_dependents = random.randint(0, 3)  # 0-3 dependents
        
        cube = ClusterCube(
            cube_id=f"{circlverse_id}_HH{i+1:03d}",
            num_dots=num_dots,
            num_dependents=num_dependents,
            savings_rate=random.uniform(0.05, 0.25)  # 5-25% savings rate
        )
        
        cv.add_cluster_cube(cube)
    
    return cv


def create_manual_circlverse(
    circlverse_id: str,
    household_configs: List[Dict],
    radius: float = 100.0,
    economic_multiplier: float = 1.0,
    cost_of_living_index: float = 1.0
) -> Circlverse:
    """
    Create a Circlverse with manually specified households
    
    Args:
        circlverse_id: Unique identifier
        household_configs: List of dicts with keys:
            - num_dots: int (1-6)
            - num_dependents: int (optional, default 0)
            - occupations: List[str] (optional, default random)
            - savings_rate: float (optional, default 0.15)
            - initial_wealth: float (optional, default 0.0)
        radius: Radius of the circular town
        economic_multiplier: Economic health
        cost_of_living_index: Cost multiplier
    """
    cv = Circlverse(
        circlverse_id=circlverse_id,
        radius=radius,
        economic_multiplier=economic_multiplier,
        cost_of_living_index=cost_of_living_index
    )
    
    for i, config in enumerate(household_configs):
        num_dots = config.get('num_dots', random.randint(1, 6))
        num_dependents = config.get('num_dependents', 0)
        savings_rate = config.get('savings_rate', 0.15)
        
        # Create dots with specified occupations if provided
        dots = []
        occupations_list = config.get('occupations', [])
        
        if occupations_list:
            for j, occ_name in enumerate(occupations_list[:num_dots]):
                try:
                    occupation = OccupationType(occ_name.lower())
                except ValueError:
                    occupation = OccupationType.UNEMPLOYED
                
                age = random.randint(25, 65) if j == 0 else random.randint(0, 80)
                is_working = (age >= 18 and age <= 65 and occupation != OccupationType.UNEMPLOYED)
                dots.append(Dot(age=age, occupation=occupation, is_working=is_working))
        
        cube = ClusterCube(
            cube_id=f"{circlverse_id}_HH{i+1:03d}",
            num_dots=num_dots,
            num_dependents=num_dependents,
            savings_rate=savings_rate,
            dots=dots if dots else None,  # Will auto-generate if None
            current_wealth=config.get('initial_wealth', 0.0)
        )
        
        cv.add_cluster_cube(cube)
    
    return cv


def create_simulation_from_config(
    num_circlverses: int,
    households_per_circlverse: int,
    random_config: bool = True,
    manual_configs: Optional[List[Dict]] = None
) -> CircleverseSimulation:
    """
    Create a complete simulation from configuration
    
    Args:
        num_circlverses: Number of towns to create
        households_per_circlverse: Number of households per town
        random_config: If True, use random configuration
        manual_configs: If provided and random_config=False, use these configs
            Format: List of dicts, each dict can have:
            - households: List of household config dicts (see create_manual_circlverse)
            - radius: float
            - economic_multiplier: float
            - cost_of_living_index: float
    """
    simulation = CircleverseSimulation()
    
    if random_config:
        for i in range(num_circlverses):
            cv = create_random_circlverse(
                circlverse_id=f"Town_{i+1:02d}",
                num_households=households_per_circlverse
            )
            simulation.add_circlverse(cv)
    else:
        if manual_configs is None:
            raise ValueError("manual_configs required when random_config=False")
        
        for i, config in enumerate(manual_configs):
            cv_id = config.get('circlverse_id', f"Town_{i+1:02d}")
            household_configs = config.get('households', [])
            
            cv = create_manual_circlverse(
                circlverse_id=cv_id,
                household_configs=household_configs,
                radius=config.get('radius', 100.0),
                economic_multiplier=config.get('economic_multiplier', 1.0),
                cost_of_living_index=config.get('cost_of_living_index', 1.0)
            )
            simulation.add_circlverse(cv)
    
    return simulation


def create_example_simulation() -> CircleverseSimulation:
    """
    Create an example simulation with 2-3 Circlverses and 10-20 households each
    Demonstrates different economic scenarios
    """
    simulation = CircleverseSimulation()
    
    # Town 1: Prosperous town (high income, moderate cost)
    cv1 = create_random_circlverse(
        circlverse_id="Prosperity",
        num_households=15,
        economic_multiplier=1.4,  # High economic multiplier
        cost_of_living_index=1.1  # Moderate cost of living
    )
    simulation.add_circlverse(cv1)
    
    # Town 2: Struggling town (low income, high cost)
    cv2 = create_random_circlverse(
        circlverse_id="Struggleville",
        num_households=18,
        economic_multiplier=0.7,  # Low economic multiplier
        cost_of_living_index=1.3  # High cost of living
    )
    simulation.add_circlverse(cv2)
    
    # Town 3: Balanced town (average everything)
    cv3 = create_random_circlverse(
        circlverse_id="Balance",
        num_households=12,
        economic_multiplier=1.0,  # Average
        cost_of_living_index=1.0  # Average
    )
    simulation.add_circlverse(cv3)
    
    return simulation
