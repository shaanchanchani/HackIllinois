import pandas as pd
import os
import requests
import json
import csv
import io

def nassRequest_pr(folder_path):
    
    def pull_pr_Data(url,cropNames, CropsOfInterest,folder_path):
        for i in range(0,4):
            # API parameters
            params = {
                    "key": "",
                    "source_desc": "SURVEY",
                    "sector_desc": "CROPS",
                    "short_desc": CropsOfInterest[i],
                    "agg_level_desc": "STATE",
                    "year__GE": "2000",
                    "freq_desc" : "MONTHLY",
                    "format": "JSON"
                }
            response = requests.get(url, params=params)
            if response.status_code == 200:      
                data = json.loads(response.text)            
                if "data" in data:            
                    filename = cropNames[i] 
                    csv_path = os.path.join(folder_path, f"{filename}.csv")
                    with open(csv_path, "w", newline = "") as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(["state", "item", "year", "month", "yield_value"])
                        for result in data["data"]:
                            state = result["state_name"]
                            yield_value = result["Value"]
                            year_val = result["year"]
                            month = result["reference_period_desc"]
                            item = result["short_desc"]
                            writer.writerow([state,item,year_val,month,yield_value])
                else:
                    print("API request was successful, but no data was returned.")
            else:
                print(f"Error: API request failed with status code {response.status_code}")
    
    def pull_yield_Data(url,CropsOfInterest):
        for crop in CropsOfInterest:
            # API parameters
            params = {
                "key": "",
                "source_desc": "SURVEY",
                "sector_desc": "CROPS",
                "commodity_desc": crop,
                "agg_level_desc": "STATE",
                "statisticcat_desc": "YIELD",
                "year__GE": "2022",
                "format": "JSON"
            }
            outputFolderPath = "./opdata2"

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = json.loads(response.text)

                if "data" in data:
                    filename = crop + "_STATES_2022"
                    csv_path = os.path.join(outputFolderPath, f"{filename}.csv")

                    with open(csv_path, "w", newline = "") as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(["state", "item", "year", "yield_value"])

                        for result in data["data"]:
                            state = result["state_name"]
                            yield_value = result["Value"]
                            year = result["year"]
                            item = result["short_desc"]
                            writer.writerow([state,item,year,yield_value])
                else:
                    print("API request was successful, but no data was returned.")
            else:
                print(f"Error: API request failed with status code {response.status_code}")
        
    def clean_pr_data(folder_path):
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

        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):

                df = pd.read_csv(os.path.join(folder_path, filename))
                
                df = df.drop(columns=["item"])
                df = df.rename(columns={"yield_value": "price_received"})
                df["price_received"] = df["price_received"].apply(pd.to_numeric, errors="coerce")
                df = df.dropna(subset=["price_received"])
                df["month"] = df["month"].map(month_dict)

                df.to_csv(os.path.join(folder_path, filename), index=False)


  
    url = "https://quickstats.nass.usda.gov/api/api_GET/"
    cropNames = ["BARLEY", "CORN", "OATS", "SOYBEANS"]
    CropsOfInterest = ["BARLEY - PRICE RECEIVED, MEASURED IN $ / BU", "CORN, GRAIN - PRICE RECEIVED, MEASURED IN $ / BU", "OATS - PRICE RECEIVED, MEASURED IN $ / BU", "SOYBEANS - PRICE RECEIVED, MEASURED IN $ / BU" ]

    #pull_pr_Data(url,cropNames, CropsOfInterest, "./pr")
    #pull_yield_Data()
    #clean_pr_data("./pr")

    states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Conneticut',    'Delaware',    'Florida',    'Georgia',    'Hawaii',    'Idaho',    'Illinois',    'Indiana',    'Iowa',    'Kansas',    'Kentucky',    'Louisiana',    'Maine',    'Maryland',    'Massachusetts',    'Michigan',    'Minnesota',    'Mississippi',    'Missouri',    'Montana',    'Nebraska',    'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

    years = range(2000, 2023)
    months = range(1, 13)
    keys = []

    for state in states:
        for year in years:
            for month in months:
                keys.append((state, year, month))

    df = pd.DataFrame(keys, columns=['state', 'year', 'month'])

    df['key'] = df.apply(lambda x: (x['state'], x['year'], x['month']), axis=1)

    df = df.assign(BARLEY=None, CORN=None, OATS=None, SOYBEANS=None)
    
    for filename in os.listdir(folder_path):
            df_toBmerged = pd.read_csv(os.path.join(folder_path,filename))
            cropname = filename.split(".")[0]
            df_toBmerged['key'] = df_toBmerged.apply(lambda x: (x['state'], x['year'], x['month']), axis=1)
            for index,key in df_toBmerged['key'].items():
                    df.loc[df['key'] == key, cropname] = df_toBmerged.loc[index, 'price_received']

    df = df.dropna(subset=['BARLEY', 'CORN', 'OATS', 'SOYBEANS'],how='all')
    return df 

def main():
    folder_path = "./pr"

if __name__ == "__main__":
    main()