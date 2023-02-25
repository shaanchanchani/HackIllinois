import requests
import json
import os
import csv


def main():
    # API endpoint
    url = "https://quickstats.nass.usda.gov/api/api_GET/"

    CropsOfInterest = ["CORN", "SOYBEANS", "BARLEY", "OATS"]

    for crop in CropsOfInterest:
        # API parameters
        params = {
            "key": "7EAD1CE2-43DC-349C-BA7D-6AB559C9CDF3",
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

        # Check if response is successful
        if response.status_code == 200:
            # Parse JSON response
            data = json.loads(response.text)
            # Check if the response contains data
            if "data" in data:
                # Print results
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

            
if __name__ == "__main__":
    main()