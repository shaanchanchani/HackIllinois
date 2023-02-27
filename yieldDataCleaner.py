import pandas as pd
import os


def cleanCSV(folder_path):
    # Loop through each file in the directory
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Read the CSV file into a Pandas DataFrame
            df = pd.read_csv(os.path.join(folder_path, filename))
            
            # Drop duplicates based on the "state" column and keep the first occurrence
            df.drop_duplicates(subset=["state"], keep="first", inplace=True)
            df["item"] = df["item"].str.split(n=1).str[0]
            df = df[~df["state"].str.contains("OTHER STATES")]
            df["item"] = df["item"].str.replace(r"[^a-zA-Z]+", "", regex=True)


            # Write the updated DataFrame back to the CSV file
            df.to_csv(os.path.join(folder_path, filename), index=False)


def func(folder_path):
    op_path = "./testdata"
    for filename in os.listdir(folder_path):

        if filename.endswith(".csv"):
            name_index = filename.find('_')
            crop_name = filename[:name_index]
            df = pd.read_csv(os.path.join(folder_path, filename))


            df = df.drop(columns = "item")
            df = df.rename(columns={"yield_value": crop_name})
            df.to_csv(os.path.join(op_path, filename), index=False)

def func2(folder_path):
    op_path = "./testdata"
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Get list of unique (state, item, year) combinations across all files
    unique_combos = set()
    for filename in csv_files:
        temp_df = pd.read_csv(os.path.join(folder_path, filename))
        for index, row in temp_df.iterrows():
            unique_combos.add(row['state'])

    # Create empty dataframe with index of unique (state, item, year) combinations
    df = pd.DataFrame(index=list(unique_combos), columns=['value'])

    # Fill in values for each cell by looping through CSV files
    for filename in csv_files:
        name_index = filename.find('_')
        crop_name = filename[:name_index]

        temp_df = pd.read_csv(os.path.join(folder_path, filename))
        for index, row in temp_df.iterrows():
            state = row['state']
            value = row.iloc[-1]
            df.loc[state, 'value'] = value

    # Reset index to columns and rename them
    df = df.reset_index().rename(columns={'level_0': 'state', 'level_1': 'item', 'level_2': 'year'})
    df.to_csv(os.path.join(op_path, filename), index=False)


def func3(folder_path):
    states = ['ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA', 'COLORADO',          'CONNECTICUT', 'DELAWARE', 'FLORIDA', 'GEORGIA', 'HAWAII', 'IDAHO',          'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS', 'KENTUCKY', 'LOUISIANA',          'MAINE', 'MARYLAND', 'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA',          'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA', 'NEVADA',          'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK',          'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA', 'OREGON',          'PENNSYLVANIA', 'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA',          'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT', 'VIRGINIA', 'WASHINGTON',          'WEST VIRGINIA', 'WISCONSIN', 'WYOMING']
    print(len(states))

def main():
    folder_path = "./yield"


    #cleanCSV(folder_path)

    #func(folder_path)
    func3(folder_path)

if __name__ == "__main__":
    main()