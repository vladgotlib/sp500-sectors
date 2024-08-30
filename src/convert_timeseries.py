import pandas as pd
import json
import os
from datetime import datetime
from utils.find_nested_key import find_nested_key_fn

def load_raw_file(file):
    # Parse the JSON data
    try:
        with open(file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file) 

            print(f"Processing file: {json_file}")

            # Extract the 'indexLevels' list
            index_levels = find_nested_key_fn(data, "indexLevels")

            # Create a DataFrame
            filtered_data = [{k: d[k] for k in ("effectiveDate", "indexValue")} for d in index_levels]

            df = pd.DataFrame(filtered_data)

            # Convert 'effectiveDate' from Unix time (milliseconds) to datetime
            df['effectiveDate'] = pd.to_datetime(df['effectiveDate'], unit='ms').dt.date

            # Set 'effectiveDate' as the index
            df.set_index('effectiveDate', inplace=True)

            # Rename the 'indexValue' column to the filename (without extension)
            column_name = os.path.splitext(os.path.basename(file))[0].replace(" ", "")
            df.rename(columns={"indexValue": column_name}, inplace=True)
            
            # The resulting DataFrame
            return df
    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Function to normalize a single column, handling NaN and zero cases
def normalize_series(series):
    first_value = series.iloc[0]
    
    if pd.isna(first_value) or first_value == 0:
        # Handling the NaN or zero cases
        # Option 1: Forward-fill the first value if it's NaN or zero
        first_value = series.ffill().iloc[0]
        
        # Option 2: Replace with a small number to avoid division by zero (if you prefer)
        # first_value = 0.0001 if first_value == 0 else first_value
        
        # If the series is still invalid, return NaN for the entire column
        if pd.isna(first_value) or first_value == 0:
            return pd.Series([pd.NA] * len(series), index=series.index)
    
    # Normalize the series
    return (series / first_value) * 100