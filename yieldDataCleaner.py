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

def main():
    folder_path = "./opdata"

    cleanCSV(folder_path)


if __name__ == "__main__":
    main()