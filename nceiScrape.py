import requests 
import datetime as dt
import pandas as pd
import requests
import io
import csv

#Input: List of urls to scrape data from
#Output: Generates csv files within a folder titled "historical" in directory
def pullData(feature_urls):
    for feature in feature_urls:
        response = requests.get(feature)

        if response.status_code == 200:
            content = response.content.decode('utf-8')
            reader = csv.reader(io.StringIO(content))                         # Check if response is successful
            csv_path = f"./historical/{feature}.csv"
            with open(csv_path, "w", newline = "") as csv_file:
                writer = csv.writer(csv_file)
                for row in reader:
                    writer.writerow(row)


def main():
    pcp = "https://www.ncei.noaa.gov/pub/data/cirs/climdiv/climdiv-pcpnst-v1.0.0-20230206"
    tmax = "https://www.ncei.noaa.gov/pub/data/cirs/climdiv/climdiv-tmaxst-v1.0.0-20230206"
    tmin = "https://www.https://www.ncei.noaa.gov/pub/data/cirs/climdiv/climdiv-tminst-v1.0.0-20230206"

    feature_urls = [pcp,tmax,tmin]

    pullData(feature_urls)

    features = ["pcp", "tmax", "tmin"]



if __name__ == "__main__":
    main()