import pandas as pd
import json
import csv
import os
import numpy as np

# Function to create folder if it doesn't exist
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("restart script, empty folder -> " + folder_path)
        quit()

# function that return the names of csv's key csv 
def find_key_csv(input_path):
    input_filename = os.path.basename(input_path)
    key_filename = input_filename.replace("_output.csv", "_output_keys.csv")
    key_csv = os.path.join(input_folder, key_filename)
    
    if os.path.exists(key_csv):
        return key_csv
    else:
        print("Key CSV file not found.")
        return None

# fill in the key gap
def fill_key(df):
    df[df["Keys"]==""] = np.nan
    df["Keys"].fillna(method='ffill', inplace=True)
    return df

# drop empty value column to reduce df size
def drop_col(df):
    nan_value = float("NaN") 
    df.replace("", nan_value, inplace=True) 
    df.dropna(how='all', axis=1, inplace=True) 
    return df

def json_to_csv(input_path, output_path):
    with open(input_path) as json_file:
        data = json.load(json_file)
    df = pd.DataFrame()
    df["Keys"] = None
    keys = list(data.keys())
    for k in keys:
        entry = pd.json_normalize(data[k])
        df = df._append(entry, ignore_index = True)
        df.at[len(df)-1, "Keys"] = k
    update_df = fill_key(df)
    
    # Write DataFrame to CSV
    csv_filename = os.path.splitext(os.path.basename(output_path))[0]
    update_df.to_csv(output_path, index=False)
    print(f"Write to {output_path} completed.")

def csv_to_json(csv_path, output_path):
   # Read CSV file
    df = pd.read_csv(csv_path) 
    # Construct JSON data
    json_data = {}
    # sort csv by Keys
    key_group = df.groupby(["Keys"])
    for key in key_group.groups:
        j_df = (df.loc[key_group.groups[key]]).drop(columns=['Keys'])
        update_j_df = drop_col(j_df)
        # j = update_j_df.to_json(orient="records")
        json_data[key] = update_j_df
    # Write JSON data to file
    with open(output_path, 'w') as json_file:
        json.dumps(json_data, json_file, indent=4)
    
    print(f"Conversion from CSV to JSON completed. JSON file saved at {output_path}")

def main(input_path, output_path):
    create_folder(input_path)
    create_folder(output_path)
    input_files = [os.path.join(input_path, file) for file in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, file))]
    
    for file in input_files:
        base_name, ext = os.path.splitext(os.path.basename(file))
        output_file = os.path.join(output_path, f"{base_name}_output.json" if ext.lower() == ".csv" else f"{base_name}_output.csv")
        
        if ext.lower() == ".csv":
            # key = find_key_csv(file)
            csv_to_json(file, output_file)
        elif ext.lower() == ".json":
            json_to_csv(file, output_file)
        else:
            print(f"Unsupported file format for file: {file}")

   
if __name__ == "__main__":
    input_folder = './input/'
    output_folder = './output/'
    main(input_folder, output_folder)
