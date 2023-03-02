import requests
import json
import csv

def main():
    token = "" 
    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    params = {
        "datasetid": "GHCND",
        "startdate": "2000-01-01",
        "enddate": "2022-12-31",
        "units": "metric",
        "limit": 1000,  # maximum number of results per query
    }

    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
          "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
          "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
          "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
          "WI", "WY"]


    with open("./cdoData/temps.csv", mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        header_row = ["state", "year", "month", "precipitation"]
        csv_writer.writerow(header_row)

        # Loop through each state and retrieve data for each year and month
        for state in states:
            print("Retrieving data for", state)
            params["locationid"] = f"FIPS:{state}"
            for year in range(2000, 2023):
                params["startdate"] = f"{year}-01-01"
                params["enddate"] = f"{year}-12-31"
                avg_temps = {}  # dictionary to store average temperatures for each month
                # Retrieve temperature data
                params["datatypeid"] = "RHUM"
                response = requests.get(url, headers={"token": "gmSzxnzUGARoSLqbKAapUAwRVdnPhApk"}, params=params)
                if response.status_code == 200:
                    data = json.loads(response.text)
                    if "results" in data:
                        # Loop through results and calculate average temperature for each month
                        for result in data["results"]:
                            month = result["date"][5:7]
                            temperature = result["value"]
                            if month not in avg_temps:
                                avg_temps[month] = [temperature]
                            else:
                                avg_temps[month].append(temperature)
                        # Write average temperature for each month to CSV file
                        for month in avg_temps:
                            avg_temp = sum(avg_temps[month]) / len(avg_temps[month])
                            csv_writer.writerow([state, year, month, avg_temp, None, None, None])
                    else:
                        print("No humidity data found for", state, year)

if __name__ == "__main__":
    main()