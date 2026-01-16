import numpy as np
import pandas as pd

def run_simulation(user_numbers, n_simulations=10000):
    """
    Run a vectorized Monte Carlo simulation for La Tinka.
    Args:
        user_numbers (list/set): The 6 numbers chosen by the user.
        n_simulations (int): Number of simulated draws.
    Returns:
        dict: Results count (3, 4, 5, 6 matches)
        float: ROI estimate (This is hypothetical based on fixed prizes)
    """
    if len(user_numbers) != 6:
        return None, 0

    user_set = np.array(list(user_numbers))
    
    # 1. Generate Winning Numbers Matrix (n_simulations x 6)
    # Range 1-50. We need unique numbers per row.
    # While np.random.choice isn't strictly unique per row in 2D, for speed we can 
    # generate a pool and reshape, or use a method to ensure uniqueness.
    # For speed in Tinka (50 numbers), standard generating loop or pool sampling is needed.
    # Fast approximation:
    rng = np.random.default_rng()
    
    # Efficient way: Generate many numbers and reshape? No, uniqueness constraint is row-wise.
    # Correct vectorized way: Argpartition on random data or loop with pre-allocation.
    # Given 10k sim is small, a loop with list comp is actually fast enough (<0.5s).
    
    sim_draws = np.zeros((n_simulations, 6), dtype=int)
    # Using python loop for uniqueness logic per draw which is tricky to vectorize fully without complex logic
    # But 10,000 is small.
    for i in range(n_simulations):
        sim_draws[i] = rng.choice(50, size=6, replace=False) + 1
        
    # 2. Vectorized Comparison
    # We broadcast user_set across the matrix
    # matches = np.isin(sim_draws, user_set).sum(axis=1) # Accurate count
    matches = np.isin(sim_draws, user_set).sum(axis=1)
    
    # 3. Aggregation
    unique, counts = np.unique(matches, return_counts=True)
    results = dict(zip(unique, counts))
    
    # Fill missing keys
    final_results = {k: results.get(k, 0) for k in [0, 1, 2, 3, 4, 5, 6]}
    
    # 4. ROI Calculation (Simplistic based on fixed prizes)
    # Cost: S/ 5 per play
    total_cost = n_simulations * 5
    
    # Prizes (approximate fixed values)
    # 2 aciertos + boliyapa (not simulated here) -> Ignore
    # 3 aciertos -> S/ 10
    # 4 aciertos -> S/ 100
    # 5 aciertos -> S/ 5000
    # 6 aciertos -> S/ 4,000,000 (Jackpot assumption)
    
    winnings = (final_results[3] * 10) + \
               (final_results[4] * 100) + \
               (final_results[5] * 5000) + \
               (final_results[6] * 4000000)
               
    roi_percent = ((winnings - total_cost) / total_cost) * 100
    
    return final_results, roi_percent

def calculate_cascade_prob(user_numbers, n_combos_subset):
    """
    Theoretical calc: if I play a combo of 8 numbers, what is the prob of cascade?
    This would be combinatorial, but for simulation module we keep it simple.
    """
    pass
