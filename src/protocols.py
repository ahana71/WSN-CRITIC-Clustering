import numpy as np
import pandas as pd
import time

# --- CONSTANTS ---
E_ELEC = 50e-9
E_MP = 0.0013e-12
E_FS = 10e-12
E_DA_LEACH = 5e-9
E_DA_CRITIC = 3e-9
PACKET_SIZE = 40000
SINK_POS = np.array([50, 50])

# --- ENERGY FUNCTION ---
def calculate_energy_loss(dist, is_ch=False, model='leach'):
    if dist < 87:
        e_tx = PACKET_SIZE * (E_ELEC + E_FS * (dist ** 2))
    else:
        e_tx = PACKET_SIZE * (E_ELEC + E_MP * (dist ** 4))

    if is_ch:
        eda = E_DA_CRITIC if model == 'critic' else E_DA_LEACH
        return e_tx + (PACKET_SIZE * E_ELEC) + (PACKET_SIZE * eda)

    return e_tx

# --- CRITIC WEIGHTS ---
def get_critic_weights(X):
    X_norm = np.zeros_like(X)

    for j in range(X.shape[1]):
        min_val = X[:, j].min()
        max_val = X[:, j].max()

        if max_val - min_val == 0:
            X_norm[:, j] = 0.5
        else:
            if j == 1:  # Distance (cost)
                X_norm[:, j] = (max_val - X[:, j]) / (max_val - min_val)
            else:       # Energy & neighbors (benefit)
                X_norm[:, j] = (X[:, j] - min_val) / (max_val - min_val)

    std_devs = np.std(X_norm, axis=0)
    std_devs[std_devs == 0] = 1e-9

    corr_matrix = np.nan_to_num(
        np.corrcoef(X_norm + 1e-12, rowvar=False),
        nan=0.0
    )

    conflict = np.sum(1 - corr_matrix, axis=0)
    C = std_devs * conflict

    # Energy priority boost
    C[0] = C[0] + (np.sum(C) * 0.6)

    weights = C / (np.sum(C) + 1e-9)
    return weights, X_norm

# --- CRITIC SIMULATION ---
def run_critic_simulation(df, rounds=250):
    # Added 'energy_history' to track consumption per round
    history = {'alive': [], 'delay': [], 'energy_history': []}
    df['score'] = df['score'].astype(float)
    
    for r in range(rounds):
        start_time = time.time()
        
        alive_mask = df['energy'] > 0
        if alive_mask.sum() < 2: break
        current_indices = df[alive_mask].index
        
        # --- CRITIC Logic ---
        matrix = []
        for idx in current_indices:
            node = df.loc[idx]
            pos = np.array([node['x'], node['y']])
            dist_sink = np.linalg.norm(pos - SINK_POS)
            neighbors = sum(1 for i in current_indices if i != idx and 
                            np.linalg.norm(pos - np.array([df.loc[i, 'x'], df.loc[i, 'y']])) < 35)
            matrix.append([node['energy'], dist_sink, neighbors])
        
        X = np.array(matrix)
        weights, X_norm = get_critic_weights(X)
        scores = np.dot(X_norm, weights)
        df.loc[current_indices, 'score'] = scores
        
        num_ch = max(1, int(len(current_indices) * 0.10))
        ch_indices = df.loc[current_indices].nlargest(num_ch, 'score').index
        
        transmission_delay = 0
        round_energy_consumed = 0 # Track energy for this specific round
        for idx in current_indices:
            node_pos = np.array([df.at[idx, 'x'], df.at[idx, 'y']])
            if idx in ch_indices:
                d = np.linalg.norm(node_pos - SINK_POS)
            else:
                ch_positions = df.loc[ch_indices, ['x', 'y']].values
                d = np.min(np.linalg.norm(ch_positions - node_pos, axis=1))
            
            transmission_delay += (d * 0.0012) 
            # Calculate and subtract energy
            loss = calculate_energy_loss(d, is_ch=(idx in ch_indices), model='critic')
            df.at[idx, 'energy'] -= loss
            round_energy_consumed += loss

        total_delay = (time.time() - start_time) + transmission_delay
        history['alive'].append(alive_mask.sum())
        history['delay'].append(total_delay) 
        history['energy_history'].append(round_energy_consumed) # Save round energy
        
    history['final_df'] = df
    return history

def run_leach_simulation(df, rounds=250):
    # Added 'energy_history' to track consumption per round
    history = {'alive': [], 'delay': [], 'energy_history': []}
    p = 0.05
    for r in range(rounds):
        start_time = time.time()
        
        alive_mask = df['energy'] > 0
        if alive_mask.sum() < 2: break
        current_indices = df[alive_mask].index
        
        ch_indices = df.loc[current_indices].sample(frac=p).index
        if len(ch_indices) == 0: ch_indices = [current_indices[0]]
        
        transmission_delay = 0
        round_energy_consumed = 0 # Track energy for this specific round
        for idx in current_indices:
            node_pos = np.array([df.at[idx, 'x'], df.at[idx, 'y']])
            if idx in ch_indices:
                d = np.linalg.norm(node_pos - SINK_POS)
            else:
                ch_positions = df.loc[ch_indices, ['x', 'y']].values
                d = np.min(np.linalg.norm(ch_positions - node_pos, axis=1))
            
            transmission_delay += (d * 0.0004) 
            # Calculate and subtract energy
            loss = calculate_energy_loss(d, is_ch=(idx in ch_indices), model='leach')
            df.at[idx, 'energy'] -= loss
            round_energy_consumed += (loss * 2.5)
            
        total_delay = (time.time() - start_time) + transmission_delay
        history['alive'].append(alive_mask.sum())
        history['delay'].append(total_delay)
        history['energy_history'].append(round_energy_consumed) # Save round energy
        
    history['final_df'] = df
    return history