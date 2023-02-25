import requests
import json
import os
import csv


def main():
    # API endpoint
    url = "https://quickstats.nass.usda.gov/api/api_GET/"

    cropNames = ["BARLEY", "CORN", "OATS", "SOYBEANS"]
    CropsOfInterest = ["BARLEY - PRICE RECEIVED, MEASURED IN $ / BU", "CORN, GRAIN - PRICE RECEIVED, MEASURED IN $ / BU", "OATS - PRICE RECEIVED, MEASURED IN $ / BU", "SOYBEANS - PRICE RECEIVED, MEASURED IN $ / BU" ]
    years = [str(i) for i in range(2000,2023)]

    # for year in years:
    for i in range(0,4):
        # API parameters
        params = {
            "key": "7EAD1CE2-43DC-349C-BA7D-6AB559C9CDF3",
            "source_desc": "SURVEY",
            "sector_desc": "CROPS",
            "short_desc": CropsOfInterest[i],
            "agg_level_desc": "STATE",
            "year__GE": "2000",
            "freq_desc" : "MONTHLY",
            "format": "JSON"
        }
        outputFolderPath = "./opdata2"

        response = requests.get(url, params=params)
        if response.status_code == 200:         # Check if response is successful
            data = json.loads(response.text)             # Parse JSON response
            if "data" in data:             # Check if the response contains data
                filename = cropNames[i] 
                csv_path = os.path.join(outputFolderPath, f"{filename}.csv")
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

            
if __name__ == "__main__":
    main()