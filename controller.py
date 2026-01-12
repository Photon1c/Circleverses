"""
Circleverse Interactive Controller
Provides command-line interface for controlling simulations
"""

import sys
from simulation import CircleverseSimulation
from setup import create_example_simulation, create_random_circlverse, create_simulation_from_config
from visualization import visualize_simulation, print_statistics, plot_wealth_distribution
import matplotlib.pyplot as plt


class SimulationController:
    """Interactive controller for Circleverse simulations"""
    
    def __init__(self, simulation: CircleverseSimulation = None):
        self.simulation = simulation or create_example_simulation()
        self.running = True
    
    def print_menu(self):
        """Print command menu"""
        print("\n" + "="*60)
        print("CIRCLEVERSE SIMULATION CONTROLLER")
        print("="*60)
        print(f"Current Month: {self.simulation.current_month}")
        print(f"Status: {'PAUSED' if self.simulation.is_paused else 'RUNNING'}")
        print("\nCommands:")
        print("  [s]tep <N>        - Step simulation N months (default: 1)")
        print("  [r]un <N>         - Run simulation until month N")
        print("  [p]ause           - Pause simulation")
        print("  [u]npause         - Resume simulation")
        print("  [v]isualize       - Show visualization")
        print("  [stats]           - Print statistics")
        print("  [hist]ogram       - Show wealth distribution histogram")
        print("  [e]xport <file>   - Export data to CSV")
        print("  [r]eset           - Reset simulation to month 0")
        print("  [q]uit            - Exit")
        print("="*60)
    
    def handle_command(self, command: str) -> bool:
        """
        Handle a command. Returns False if should quit.
        """
        parts = command.strip().split()
        if not parts:
            return True
        
        cmd = parts[0].lower()
        
        try:
            if cmd in ['s', 'step']:
                n = int(parts[1]) if len(parts) > 1 else 1
                self.simulation.step(n)
                print(f"Stepped {n} month(s). Current month: {self.simulation.current_month}")
            
            elif cmd in ['r', 'run']:
                if len(parts) > 1:
                    target = int(parts[1])
                    self.simulation.run_until(target)
                    print(f"Ran until month {target}. Current month: {self.simulation.current_month}")
                else:
                    print("Usage: run <target_month>")
            
            elif cmd in ['p', 'pause']:
                self.simulation.pause()
                print("Simulation paused.")
            
            elif cmd in ['u', 'unpause', 'resume']:
                self.simulation.resume()
                print("Simulation resumed.")
            
            elif cmd in ['v', 'visualize', 'viz']:
                print("Generating visualization...")
                fig = visualize_simulation(self.simulation)
                plt.show(block=False)
                print("Visualization displayed.")
            
            elif cmd == 'stats':
                print_statistics(self.simulation)
            
            elif cmd in ['hist', 'histogram']:
                fig, ax = plt.subplots(1, 1, figsize=(8, 6), facecolor="#101010")
                plot_wealth_distribution(ax, self.simulation)
                plt.show(block=False)
                print("Histogram displayed.")
            
            elif cmd in ['e', 'export']:
                filename = parts[1] if len(parts) > 1 else "circleverse_export.csv"
                self.simulation.export_to_csv(filename)
                print(f"Data exported to {filename}")
            
            elif cmd == 'reset':
                self.simulation.reset()
                print("Simulation reset to month 0.")
            
            elif cmd in ['q', 'quit', 'exit']:
                return False
            
            else:
                print(f"Unknown command: {cmd}")
                print("Type 'help' or press Enter to see menu")
        
        except Exception as e:
            print(f"Error: {e}")
        
        return True
    
    def run_interactive(self):
        """Run interactive command loop"""
        print("\nWelcome to Circleverse Simulation Controller!")
        self.print_menu()
        
        while self.running:
            try:
                command = input("\n> ").strip()
                if command.lower() in ['help', 'h', '?', '']:
                    self.print_menu()
                else:
                    self.running = self.handle_command(command)
            except KeyboardInterrupt:
                print("\n\nInterrupted. Exiting...")
                break
            except EOFError:
                break
        
        print("Goodbye!")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Circleverse Simulation Controller")
    parser.add_argument('--example', action='store_true', 
                       help='Use example simulation')
    parser.add_argument('--random', type=int, nargs=2, metavar=('NUM_CV', 'NUM_HH'),
                       help='Create random simulation with NUM_CV circlverses and NUM_HH households each')
    parser.add_argument('--run', type=int, metavar='MONTHS',
                       help='Run simulation for MONTHS and exit')
    parser.add_argument('--export', type=str, metavar='FILE',
                       help='Export data to FILE and exit')
    parser.add_argument('--visualize', action='store_true',
                       help='Show visualization and exit')
    
    args = parser.parse_args()
    
    # Create simulation
    if args.random:
        num_cv, num_hh = args.random
        sim = CircleverseSimulation()
        for i in range(num_cv):
            cv = create_random_circlverse(f"Town_{i+1:02d}", num_hh)
            sim.add_circlverse(cv)
    else:
        sim = create_example_simulation()
    
    controller = SimulationController(sim)
    
    # Handle non-interactive modes
    if args.run:
        sim.run_until(args.run)
        print_statistics(sim)
    
    if args.export:
        sim.export_to_csv(args.export)
        print(f"Data exported to {args.export}")
    
    if args.visualize:
        fig = visualize_simulation(sim)
        plt.show()
    
    # If no flags or only --run/--export, run interactive
    if not any([args.run, args.export, args.visualize]) or args.run:
        controller.run_interactive()


if __name__ == "__main__":
    main()
