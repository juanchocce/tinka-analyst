import pandas as pd
import numpy as np
import scipy.stats as stats
from itertools import combinations
from collections import Counter

def get_gap_metrics(df_exploded, current_sorteo_max):
    """
    Calculates Gap Analysis: Mean Gap, Current Lag, and Z-Score for 'Pressure'.
    """
    gaps = {}
    for num in range(1, 51):
        # Sort desc by Sorteo ID
        # Assuming 'Sorteo' column exists and is numeric or sortable
        draws_with_num = df_exploded[df_exploded['Numero'] == num]['Sorteo'].astype(str).str.extract('(\d+)').astype(int).squeeze().sort_values(ascending=False).values
        
        if len(draws_with_num) > 1:
            diffs = np.abs(np.diff(draws_with_num))
            mean_gap = np.mean(diffs)
            std_gap = np.std(diffs)
            last_seen = draws_with_num[0]
            current_gap = current_sorteo_max - last_seen
            
            # Z-Score: (Current - Mean) / Std
            z_score = (current_gap - mean_gap) / std_gap if std_gap > 0 else 0
            
            gaps[num] = {
                'Numero': num,
                'Mean_Gap': mean_gap,
                'Current_Gap': current_gap,
                'Z_Score': z_score
            }
        else:
            gaps[num] = {'Numero': num, 'Mean_Gap': 0, 'Current_Gap': 0, 'Z_Score': 0}
            
    return pd.DataFrame(gaps).T

def get_markov_matrix(df_draws, bins=[0, 130, 150, 170, 300], labels=['Very Low', 'Low', 'High', 'Very High']):
    """
    Calculates Transition Matrix based on Sum of balls.
    """
    df = df_draws.copy()
    df['State'] = pd.cut(df['Suma'], bins=bins, labels=labels)
    df['Next_State'] = df['State'].shift(-1) # Negative shift because data is often reverse chronological
    
    # Filter out NaNs
    df = df.dropna(subset=['State', 'Next_State'])
    
    transition_matrix = pd.crosstab(df['Next_State'], df['State'], normalize='index')
    return transition_matrix

def get_cooccurrence_matrix(df_draws):
    """
    Calculates how often pairs of numbers appear together.
    """
    pair_counts = Counter()
    for _, row in df_draws.iterrows():
        nums = sorted([int(n) for n in row['Bolillas_Clean'] if n.isdigit()])
        pair_counts.update(combinations(nums, 2))
        
    matrix = pd.DataFrame(index=range(1, 51), columns=range(1, 51)).fillna(0)
    for (a, b), count in pair_counts.items():
        matrix.loc[a, b] = count
        matrix.loc[b, a] = count
        
    return matrix

def get_entropy(df_exploded):
    """
    Calculates Shannon Entropy of the number distribution.
    """
    freqs = df_exploded['Numero'].value_counts(normalize=True)
    return stats.entropy(freqs)
