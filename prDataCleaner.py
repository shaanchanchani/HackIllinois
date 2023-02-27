import pandas as pd
import os


def clean_pr_CSV(folder_path):

    month_dict = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12
}

    # Loop through each file in the directory
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Read the CSV file into a Pandas DataFrame
            df = pd.read_csv(os.path.join(folder_path, filename))
            
            df = df.drop(columns=["item"])
            #df = df.rename(columns={"yield_value": "price_received"})
            #df["price_received"] = df["price_received"].apply(pd.to_numeric, errors="coerce")
            #df = df.dropna(subset=["price_received"])
            #df["month"] = df["month"].map(month_dict)


            # Write the updated DataFrame back to the CSV file
            df.to_csv(os.path.join(folder_path, filename), index=False)





def main():


    folder_path = "./pr"

    #clean_pr_CSV(folder_path)


if __name__ == "__main__":
    main()