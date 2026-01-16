import sys
import os

# Add current dir to path just in case
sys.path.append(os.getcwd())

try:
    print("Testing Imports...")
    from modules import etl, analysis, simulation
    print("Imports Successful.")

    print("Testing Data Loading...")
    df_draws, df_exploded = etl.load_data()
    if not df_draws.empty:
        print(f"Data Loaded Successfully. Rows: {len(df_draws)}")
        print(f"Latest Draw: {df_draws['Fecha'].max()}")
        
        print("Testing Analysis Mock...")
        entropy = analysis.get_entropy(df_exploded)
        print(f"Entropy calculated: {entropy}")
        
        print("Testing Simulation Mock...")
        res, roi = simulation.run_simulation({1,2,3,4,5,6}, n_simulations=100)
        print("Simulation ran successfully.")
        
    else:
        print("Data Load Returned Empty DF.")

except Exception as e:
    print(f"Verification Failed: {e}")
    import traceback
    traceback.print_exc()
