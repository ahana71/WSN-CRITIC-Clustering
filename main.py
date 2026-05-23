import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from src.network_env import initialize_nodes
from src.protocols import run_critic_simulation, run_leach_simulation

def get_unique_filename(prompt):
    while True:
        name = input(prompt).strip()
        if not name.endswith('.png'):
            name += '.png'
        if os.path.exists(name):
            print(f"Error: '{name}' already exists. Please enter a different name.")
        else:
            return name

def main():
    np.random.seed(42)
    print("--- Starting Simulation ---")
    
    # Initialize
    nodes_init = initialize_nodes(count=100)
    # Capture the exact initial energy value used for all sensors
    initial_energy_val = nodes_init['energy'].iloc[0] 
    
    # Run Simulations
    print("Running CRITIC Simulation...")
    critic_res = run_critic_simulation(nodes_init.copy(), rounds=2000)
    
    print("Running LEACH Simulation...")
    leach_res = run_leach_simulation(nodes_init.copy(), rounds=2000)
    
    # --- GRAPH 0: Network Lifetime (Original) ---
    plt.figure(figsize=(10, 6))
    plt.plot(critic_res['alive'], label='CRITIC-Assisted Model', color='green')
    plt.plot(leach_res['alive'], label='Standard LEACH', color='red', linestyle='--')
    plt.title('Network Lifetime: CRITIC vs LEACH')
    plt.xlabel('Rounds'); plt.ylabel('Number of Alive Nodes')
    plt.legend(); plt.grid(True)
    plt.savefig(get_unique_filename("Enter filename for Network Lifetime graph :- "))

    # --- GRAPH 3: Transmission/communication delay required (Requirement 3) ---
    plt.figure(figsize=(10, 6))
    plt.plot(critic_res['delay'], label='CRITIC Transmission Delay', color='green', alpha=0.7)
    plt.plot(leach_res['delay'], label='LEACH Transmission Delay', color='red', alpha=0.7, linestyle=':')
    plt.title("Modeled Communication Delay: CRITIC vs LEACH")
    plt.xlabel('Rounds'); plt.ylabel('Time (Seconds)')
    plt.legend(); plt.grid(True)
    plt.savefig(get_unique_filename("Enter filename for Transmission Delay graph :- "))

    # --- GRAPH 4: Individual Energy Consumed (Requirement 4) ---
    # plt.figure(figsize=(14, 7))
    # energy_consumed_critic = initial_energy_val - critic_res['final_df']['energy']
    # energy_consumed_leach = initial_energy_val - leach_res['final_df']['energy']
    # sample_size = 25
    # sensor_indices = np.arange(sample_size)
    
    # plt.bar(sensor_indices - 0.2, energy_consumed_critic[:sample_size], 0.4, 
    #         label='CRITIC Energy Consumed', color='green', alpha=0.8)
    # plt.bar(sensor_indices + 0.2, energy_consumed_leach[:sample_size], 0.4, 
    #         label='LEACH Energy Consumed', color='red', alpha=0.8)
    
    # plt.title(f'Individual Energy Consumption Comparison (First {sample_size} Sensors)')
    # plt.xlabel('Sensor ID'); plt.ylabel('Total Energy Consumed (Joules)')
    # plt.xticks(sensor_indices); plt.legend(); plt.grid(axis='y', linestyle='--', alpha=0.5)
    # plt.tight_layout()
    # plt.savefig(get_unique_filename("Enter filename for Individual Energy Consumption graph :- "))

    # --- NEW GRAPH 5: Energy Impact based on CRITIC Attributes (FIXED) ---
    # plt.figure(figsize=(10, 6))
    # attribute_labels = ['Residual Energy', 'Distance to Sink', 'Node Density']
    
    # # We use a copy to calculate distances for the analysis
    # analysis_df = critic_res['final_df'].copy()
    # analysis_df['dist_to_sink'] = np.sqrt((analysis_df['x'] - 50)**2 + (analysis_df['y'] - 50)**2)
    
    # # Calculate average energy consumed by nodes representing each attribute category
    # impact_vals = [
    #     (initial_energy_val - analysis_df.nlargest(10, 'energy')['energy']).mean(),
    #     (initial_energy_val - analysis_df.nsmallest(10, 'dist_to_sink')['energy']).mean(),
    #     (initial_energy_val - analysis_df.nlargest(10, 'energy')['energy']).mean() * 0.85 # Density approximation
    # ]

    # plt.bar(attribute_labels, impact_vals, color=['#27ae60', '#2980b9', '#e67e22'])
    # plt.title('Energy Consumption based on Selection Attributes (CRITIC)')
    # plt.ylabel('Average Energy Consumed (Joules)')
    # plt.grid(axis='y', linestyle=':', alpha=0.7)
    # plt.savefig(get_unique_filename("Enter filename for Attribute Energy Impact graph :- "))
    
    # --- NEW GRAPH 6: Total Network Residual Energy Comparison ---
    # plt.figure(figsize=(8, 6))
    # total_critic_energy = critic_res['final_df']['energy'].sum()
    # total_leach_energy = leach_res['final_df']['energy'].sum()
    
    # comparison_labels = ['CRITIC Model', 'LEACH Protocol']
    # energy_values = [total_critic_energy, total_leach_energy]
    
    # plt.bar(comparison_labels, energy_values, color=['green', 'red'])
    # plt.title('Total Network Residual Energy: CRITIC vs LEACH')
    # plt.ylabel('Total Energy Remaining (Joules)')
    
    # # Adding text labels on top of bars
    # for i, v in enumerate(energy_values):
    #     plt.text(i, v + (max(energy_values) * 0.02), f"{v:.4f}J", ha='center', fontweight='bold')
        
    # plt.grid(axis='y', linestyle='--', alpha=0.6)
    # plt.savefig(get_unique_filename("Enter filename for Total Energy Comparison graph :- "))
    
    # --- GRAPH 7: Energy Consumption per Round (Line Comparison) ---
    plt.figure(figsize=(10, 6))
    plt.plot(critic_res['energy_history'], label='CRITIC Energy Consumption', color='green', alpha=0.8)
    plt.plot(leach_res['energy_history'], label='LEACH Energy Consumption', color='red', alpha=0.8, linestyle='--')
    plt.title('Modeled Energy Consumption: CRITIC vs LEACH')
    plt.xlabel('Rounds')
    plt.ylabel('Energy Consumed (Joules)')
    plt.legend()
    plt.grid(True)
    plt.savefig(get_unique_filename("Enter filename for Energy Consumption Line graph :- "))
    
    # --- NEW GRAPH: Energy Comparison of CRITIC-Selected Sensors ---
    plt.figure(figsize=(12, 6))
    
    # Identify the top 5 sensors CRITIC prioritized (highest scores in final state)
    # These are the "sensors used by critic" for leadership
    top_critic_nodes = critic_res['final_df'].nlargest(5, 'score').index
    
    # Calculate energy consumed for these specific nodes (Initial - Final)
    energy_used_critic = [initial_energy_val - critic_res['final_df'].at[idx, 'energy'] for idx in top_critic_nodes]
    energy_used_leach = [initial_energy_val - leach_res['final_df'].at[idx, 'energy'] for idx in top_critic_nodes]
    
    x_indices = np.arange(len(top_critic_nodes))
    node_labels = [f"Sensor {idx}" for idx in top_critic_nodes]
    
    plt.bar(x_indices - 0.2, energy_used_critic, 0.4, label='Energy Used (CRITIC)', color='#27ae60')
    plt.bar(x_indices + 0.2, energy_used_leach, 0.4, label='Energy Used (LEACH)', color='#e74c3c')
    
    plt.xticks(x_indices, node_labels)
    plt.title('Energy Consumption of Top CRITIC-Selected Sensors')
    plt.ylabel('Energy Consumed (Joules)')
    plt.legend()
    plt.grid(axis='y', linestyle=':', alpha=0.7)
    plt.savefig(get_unique_filename("Enter filename for CRITIC-Selected Sensors Energy Comparison graph :- "))

    # --- CSV Export ---
    # max_len = max(len(critic_res['alive']), len(leach_res['alive']))
    # results_df = pd.DataFrame({
    #     'Round': range(max_len),
    #     'CRITIC_Alive': critic_res['alive'] + [0]*(max_len - len(critic_res['alive'])),
    #     'LEACH_Alive': leach_res['alive'] + [0]*(max_len - len(leach_res['alive'])),
    #     'CRITIC_Delay': critic_res['delay'] + [np.nan]*(max_len - len(critic_res['delay'])),
    #     'LEACH_Delay': leach_res['delay'] + [np.nan]*(max_len - len(leach_res['delay']))
    # })
    # results_df.to_csv('final_simulation_data4.csv', index=False)
    
    print("All 4 graphs saved successfully")
    plt.show()

if __name__ == "__main__":
    main()