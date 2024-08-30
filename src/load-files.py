import pandas as pd
from datetime import datetime
from utils.find_nested_key import find_nested_key_fn
import os
from convert_timeseries import load_raw_file, normalize_series

def process_json_files_in_folder(directory):
    """
    Loads multiple JSON files from a directory, processes them,
    and stitches them together into a single DataFrame.
    """
    data_frames = []

    for file_name in os.listdir(directory):
        if file_name.endswith('.json'):
            file_path = os.path.join(directory, file_name)
            df = load_raw_file(file_path)
            df_normalized = df.apply(normalize_series)

            if df_normalized is not None:
                data_frames.append(df_normalized)

    # Concatenate all DataFrames into one, aligned on the 'effectiveDate' index
    if data_frames:
        stitched_df = pd.concat(data_frames, axis=1, join='outer').sort_index()

        return stitched_df
    else:
        print("No valid dataframes to stitch together.")
        return pd.DataFrame()


result_df = process_json_files_in_folder('raw-data')
print(result_df.head())

result_df.to_csv('output/stitched_sector_indices.csv', index=True)