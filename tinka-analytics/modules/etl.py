import pandas as pd
import numpy as np

def load_data(filepath="data/tinka_data.csv"):
    """
    Load and clean the Tinka dataset.
    Returns a tuple: (df_draws, df_exploded)
    """
    try:
        df = pd.read_csv(filepath, encoding='latin1')
    except FileNotFoundError:
        return pd.DataFrame(), pd.DataFrame()

    # 1. Date Parsing (Robust)
    def parse_dates_robust(date_str):
        try:
            return pd.to_datetime(date_str, format='%d/%m/%Y')
        except:
            return pd.to_datetime(date_str, errors='coerce')

    df['Fecha_dt'] = df['Fecha'].apply(parse_dates_robust)
    
    # 2. Filter Modern Era (Rules changed ~Oct 2022 to 50 balls)
    df_modern = df[df['Fecha_dt'] >= '2022-10-01'].copy()
    
    # 3. Clean 'Bolillas' string
    # Remove extra spaces and split
    df_modern['Bolillas_Clean'] = df_modern['Bolillas'].astype(str).str.strip().str.replace('  ', ' ').str.split(' ')
    
    # 4. Feature Engineering on Draws
    def calculate_stats(row_list):
        try:
            nums = [int(n) for n in row_list if n.isdigit()]
            return pd.Series({
                'Suma': sum(nums),
                'Pares': sum(1 for n in nums if n % 2 == 0),
                'Impares': sum(1 for n in nums if n % 2 != 0),
                'Num_Set': frozenset(nums)
            })
        except:
            return pd.Series({'Suma': 0, 'Pares': 0, 'Impares': 0, 'Num_Set': frozenset()})

    df_modern = pd.concat([df_modern, df_modern['Bolillas_Clean'].apply(calculate_stats)], axis=1)
    
    # 5. Explode for Number-level analysis
    df_exploded = df_modern.explode('Bolillas_Clean')
    df_exploded['Numero'] = pd.to_numeric(df_exploded['Bolillas_Clean'], errors='coerce')
    df_exploded = df_exploded.dropna(subset=['Numero'])
    df_exploded['Numero'] = df_exploded['Numero'].astype(int)
    
    return df_modern, df_exploded
