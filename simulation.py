"""
Circleverse: Household Wealth Formation Simulation
Core simulation engine with Circlverse, ClusterCube, and Dot classes
"""

import random
import math
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum


class OccupationType(Enum):
    PROFESSIONAL = "professional"
    SKILLED_TRADE = "skilled_trade"
    SERVICE = "service"
    RETAIL = "retail"
    UNEMPLOYED = "unemployed"


# Income multipliers by occupation (monthly base income in currency units)
OCCUPATION_INCOME = {
    OccupationType.PROFESSIONAL: 8000,
    OccupationType.SKILLED_TRADE: 5000,
    OccupationType.SERVICE: 3000,
    OccupationType.RETAIL: 2500,
    OccupationType.UNEMPLOYED: 0,
}

# Expense categories (as fraction of income)
BASE_EXPENSES = {
    "housing": 0.35,
    "food": 0.15,
    "healthcare": 0.10,
    "transportation": 0.10,
    "utilities": 0.08,
    "other": 0.22,
}


@dataclass
class Dot:
    """Represents a household member (dot on a dice face)"""
    age: int
    occupation: OccupationType
    is_working: bool = True
    
    def get_monthly_income(self) -> float:
        """Calculate monthly income based on occupation"""
        base_income = OCCUPATION_INCOME.get(self.occupation, 0)
        if not self.is_working:
            return 0
        # Age-based income modifier (peak around 40-50)
        age_factor = 1.0
        if 25 <= self.age <= 50:
            age_factor = 1.2
        elif self.age < 25 or self.age > 65:
            age_factor = 0.8
        return base_income * age_factor


@dataclass
class ClusterCube:
    """
    Represents a household (like a dice cube) with dots (members)
    Positioned within a Circlverse
    """
    cube_id: str
    num_dots: int  # Number of household members (1-6, like dice)
    dots: List[Dot] = field(default_factory=list)
    num_dependents: int = 0  # Children/elderly
    location: Tuple[float, float] = (0.0, 0.0)  # x, y position in Circlverse
    
    # Financial attributes
    current_wealth: float = 0.0
    savings_rate: float = 0.15  # Fraction of net income saved
    monthly_expenses: float = 0.0
    
    # Historical tracking
    wealth_history: List[float] = field(default_factory=list)
    income_history: List[float] = field(default_factory=list)
    expense_history: List[float] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize dots if not provided"""
        if not self.dots and self.num_dots > 0:
            # Auto-generate dots with random occupations
            self.dots = self._generate_dots()
        self._calculate_base_expenses()
    
    def _generate_dots(self) -> List[Dot]:
        """Generate random household members"""
        dots = []
        occupations = list(OccupationType)
        for i in range(self.num_dots):
            age = random.randint(25, 65) if i == 0 else random.randint(0, 80)
            occupation = random.choice(occupations)
            if age < 18 or age > 65:
                occupation = OccupationType.UNEMPLOYED
            dots.append(Dot(age=age, occupation=occupation, is_working=(age >= 18 and age <= 65)))
        return dots
    
    def _calculate_base_expenses(self):
        """Calculate base monthly expenses based on household size"""
        # Base expense increases with household size
        base_housing = 1500 + (self.num_dots + self.num_dependents) * 400
        base_food = 300 + (self.num_dots + self.num_dependents) * 150
        base_other = 500 + (self.num_dots + self.num_dependents) * 100
        
        self.monthly_expenses = base_housing + base_food + base_other
    
    def get_total_income(self) -> float:
        """Calculate total household monthly income"""
        return sum(dot.get_monthly_income() for dot in self.dots)
    
    def simulate_month(self, cost_of_living_index: float = 1.0, economic_multiplier: float = 1.0):
        """
        Simulate one month of economic activity
        
        Args:
            cost_of_living_index: Local cost multiplier
            economic_multiplier: Local economic health multiplier
        """
        # Calculate income with economic multiplier
        base_income = self.get_total_income() * economic_multiplier
        
        # Apply cost of living to expenses
        expenses = self.monthly_expenses * cost_of_living_index
        
        # Add random variation (10% variance)
        expenses *= (1.0 + random.uniform(-0.1, 0.1))
        
        # Net income
        net_income = base_income - expenses
        
        # Apply savings rate
        savings = net_income * self.savings_rate if net_income > 0 else 0
        
        # Update wealth
        self.current_wealth += savings
        
        # Track history
        self.wealth_history.append(self.current_wealth)
        self.income_history.append(base_income)
        self.expense_history.append(expenses)
        
        return {
            "income": base_income,
            "expenses": expenses,
            "net_income": net_income,
            "savings": savings,
            "wealth": self.current_wealth
        }
    
    def apply_economic_shock(self, shock_type: str, magnitude: float):
        """
        Apply economic shock (job loss, medical expense, windfall)
        
        Args:
            shock_type: "job_loss", "medical", "windfall"
            magnitude: Shock magnitude (positive for windfall, negative for expenses)
        """
        if shock_type == "job_loss":
            # Randomly set one working dot to unemployed
            working_dots = [d for d in self.dots if d.is_working and d.occupation != OccupationType.UNEMPLOYED]
            if working_dots:
                dot = random.choice(working_dots)
                dot.occupation = OccupationType.UNEMPLOYED
                dot.is_working = False
        elif shock_type == "medical":
            # Large unexpected expense
            self.current_wealth += magnitude  # magnitude is negative
        elif shock_type == "windfall":
            # Unexpected income
            self.current_wealth += magnitude


@dataclass
class Circlverse:
    """
    Represents a town (circular spatial layout) containing ClusterCubes (households)
    """
    circlverse_id: str
    radius: float = 100.0  # Radius of the circular town
    economic_multiplier: float = 1.0  # Local economic health (0.5 = struggling, 1.5 = prosperous)
    cost_of_living_index: float = 1.0  # Cost multiplier (0.8 = cheap, 1.5 = expensive)
    
    cluster_cubes: List[ClusterCube] = field(default_factory=list)
    
    # Collective metrics
    total_wealth: float = 0.0
    average_wealth: float = 0.0
    wealth_history: List[float] = field(default_factory=list)
    
    def add_cluster_cube(self, cube: ClusterCube):
        """Add a household to this Circlverse"""
        # Position cube randomly within the circle
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, self.radius * 0.8)  # Leave some margin
        cube.location = (
            distance * math.cos(angle),
            distance * math.sin(angle)
        )
        self.cluster_cubes.append(cube)
    
    def simulate_month(self):
        """Simulate one month for all households in this Circlverse"""
        for cube in self.cluster_cubes:
            cube.simulate_month(
                cost_of_living_index=self.cost_of_living_index,
                economic_multiplier=self.economic_multiplier
            )
        
        # Update collective metrics
        self._update_metrics()
    
    def _update_metrics(self):
        """Update collective wealth metrics"""
        if self.cluster_cubes:
            self.total_wealth = sum(cube.current_wealth for cube in self.cluster_cubes)
            self.average_wealth = self.total_wealth / len(self.cluster_cubes)
            self.wealth_history.append(self.average_wealth)
        else:
            self.total_wealth = 0.0
            self.average_wealth = 0.0
            self.wealth_history.append(0.0)
    
    def get_wealth_distribution(self) -> Dict[str, float]:
        """Get wealth distribution statistics"""
        if not self.cluster_cubes:
            return {}
        
        wealths = [cube.current_wealth for cube in self.cluster_cubes]
        return {
            "min": min(wealths),
            "max": max(wealths),
            "mean": sum(wealths) / len(wealths),
            "median": sorted(wealths)[len(wealths) // 2],
            "total": sum(wealths)
        }
    
    def calculate_gini_coefficient(self) -> float:
        """
        Calculate Gini coefficient (0 = perfect equality, 1 = perfect inequality)
        """
        if not self.cluster_cubes or len(self.cluster_cubes) < 2:
            return 0.0
        
        wealths = sorted([cube.current_wealth for cube in self.cluster_cubes])
        n = len(wealths)
        cumsum = 0
        for i, wealth in enumerate(wealths):
            cumsum += wealth * (2 * (i + 1) - n - 1)
        
        if sum(wealths) == 0:
            return 0.0
        
        return cumsum / (n * sum(wealths))


class CircleverseSimulation:
    """
    Main simulation controller
    """
    def __init__(self):
        self.circlverses: List[Circlverse] = []
        self.current_month: int = 0
        self.is_paused: bool = False
        self.simulation_speed: int = 1  # Months per step
        
    def add_circlverse(self, circlverse: Circlverse):
        """Add a Circlverse to the simulation"""
        self.circlverses.append(circlverse)
    
    def step(self, months: int = 1):
        """Simulate N months"""
        if self.is_paused:
            return
        
        for _ in range(months):
            for circlverse in self.circlverses:
                circlverse.simulate_month()
            self.current_month += 1
    
    def run_until(self, target_month: int):
        """Run simulation until target month"""
        while self.current_month < target_month and not self.is_paused:
            self.step(1)
    
    def pause(self):
        """Pause simulation"""
        self.is_paused = True
    
    def resume(self):
        """Resume simulation"""
        self.is_paused = False
    
    def reset(self):
        """Reset simulation to month 0"""
        self.current_month = 0
        for circlverse in self.circlverses:
            for cube in circlverse.cluster_cubes:
                cube.current_wealth = 0.0
                cube.wealth_history = []
                cube.income_history = []
                cube.expense_history = []
            circlverse.wealth_history = []
    
    def get_global_statistics(self) -> Dict:
        """Get aggregate statistics across all Circlverses"""
        all_wealths = []
        for circlverse in self.circlverses:
            for cube in circlverse.cluster_cubes:
                all_wealths.append(cube.current_wealth)
        
        if not all_wealths:
            return {}
        
        return {
            "total_households": sum(len(cv.cluster_cubes) for cv in self.circlverses),
            "total_circlverses": len(self.circlverses),
            "current_month": self.current_month,
            "global_avg_wealth": sum(all_wealths) / len(all_wealths),
            "global_total_wealth": sum(all_wealths),
            "global_min_wealth": min(all_wealths),
            "global_max_wealth": max(all_wealths),
        }
    
    def export_to_csv(self, filename: str):
        """Export simulation data to CSV"""
        import csv
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Header
            writer.writerow([
                "Month", "Circlverse_ID", "Cube_ID", "Wealth", "Income", 
                "Expenses", "Num_Dots", "Num_Dependents", "Location_X", "Location_Y"
            ])
            
            # Data
            for month in range(self.current_month):
                for cv in self.circlverses:
                    for cube in cv.cluster_cubes:
                        if month < len(cube.wealth_history):
                            writer.writerow([
                                month,
                                cv.circlverse_id,
                                cube.cube_id,
                                cube.wealth_history[month],
                                cube.income_history[month] if month < len(cube.income_history) else 0,
                                cube.expense_history[month] if month < len(cube.expense_history) else 0,
                                cube.num_dots,
                                cube.num_dependents,
                                cube.location[0],
                                cube.location[1]
                            ])
