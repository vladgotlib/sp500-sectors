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
            df['effectiveDate'] = pd.to_datetime(df['effectiveDate'], unit='ms')

            # Set 'effectiveDate' as the index
            df.set_index('effectiveDate', inplace=True)

            # Rename the 'indexValue' column to the filename (without extension)
            column_name = os.path.splitext(os.path.basename(file))[0].replace(" ", "")
            df.rename(columns={"indexValue": column_name}, inplace=True)
            
            # The resulting DataFrame
            return df
    except Exception as e:
        print(f"Error processing file {file}: {e}")
