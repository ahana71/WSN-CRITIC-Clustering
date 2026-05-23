import numpy as np
import pandas as pd

# Simulation Constants
FIELD_SIZE = 300  # 100x100 meters
SINK_POS = np.array([50, 50])  # Base station in the center
INITIAL_ENERGY = 0.05 # 0.5 Joules per node

def initialize_nodes(count=100):
    """
    Creates a random distribution of sensor nodes in a 2D field.
    Each node has: ID, X, Y, and Energy.
    """
    nodes = []
    for i in range(count):
        nodes.append({
            'id': i,
            'x': np.random.uniform(0, FIELD_SIZE),
            'y': np.random.uniform(0, FIELD_SIZE),
            'energy': INITIAL_ENERGY,
            'score': 0.0  # Initial suitability score for CH selection
        })
    
    return pd.DataFrame(nodes)

def get_distance(pos1, pos2):
    """Calculates Euclidean distance between two points."""
    return np.linalg.norm(np.array(pos1) - np.array(pos2))

def is_within_range(node1, node2, radius=30):
    """Checks if two nodes are within communication range (e.g., 30m)."""
    dist = get_distance((node1['x'], node1['y']), (node2['x'], node2['y']))
    return dist <= radius