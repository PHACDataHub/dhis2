#!/opt/miniconda3/bin/python 
import pandas as pd
import json
import csv
import os

# Function to create folder if it doesn't exist
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("restart script, empty folder -> " + folder_path)
        quit()

def json_to_csv(input_path, output_path):
    with open(input_path) as json_file:
        data = json.load(json_file)
    df = pd.DataFrame()
    keys = list(data.keys())
    for k in keys:
        entry = pd.json_normalize(data[k])
        df = df._append(entry, ignore_index = True)
    filepath = output_path 
    print("write to output")
    df.to_csv(filepath)

def csv_to_json(input_path, output_path):
    df = pd.read_csv(input_path)
    filepath = output_path 
    df.to_json(filepath)

def main(input_path, output_path):
    create_folder(input_path)
    create_folder(output_path)
    input_files = [os.path.join(input_path, file) for file in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, file))]
    
    for file in input_files:
        base_name, ext = os.path.splitext(os.path.basename(file))
        output_file = os.path.join(output_path, f"{base_name}_output.json" if ext.lower() == ".csv" else f"{base_name}_output.csv")
        
        if ext.lower() == ".csv":
            csv_to_json(file, output_file)
        elif ext.lower() == ".json":
            json_to_csv(file, output_file)
        else:
            print(f"Unsupported file format for file: {file}")

   
if __name__ == "__main__":
    input_folder = './input/'
    output_folder = './output/'
    main(input_folder, output_folder)
