import datetime as dt
import meteomatics.api as api
import pandas as pd
import requests
from geopy.geocoders import Nominatim
import json
import os 
import io
import csv

def main():
    username = "purdue_chanchani"
    password = "l836KMM3jj"
    year = 2024
    startdate_ts = str(dt.datetime(year, 1, 1)).replace(" ","T") + "Z"
    enddate_ts =  str(dt.datetime(year, 12, 31)).replace(" ","T") + "Z"
    filename = "meteomatics"
    states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

    locations = []
    geolocator = Nominatim(user_agent="schancha@purdue.edu")

    for state in states:
        location = geolocator.geocode(state, exactly_one=True)
        locations.append((location.latitude, location.longitude))
        url = f"https://api.meteomatics.com/{startdate_ts}--{enddate_ts}:PT1H/t_2m:C,precip_1h:mm/{str(location.latitude)},{str(location.longitude)}/csv?access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJ2IjoxLCJ1c2VyIjoicHVyZHVlX2NoYW5jaGFuaSIsImlzcyI6ImxvZ2luLm1ldGVvbWF0aWNzLmNvbSIsImV4cCI6MTY3NzQwODk5Mywic3ViIjoiYWNjZXNzIn0.X8Ip4AOdzpsIvAZYUXI0vvCJZdeEAR0A9rzxJTjV3QuwSf_m4wzrGTGcSlFZeCN0TT9ofAwiUNa1TquSEk9XAA"

        response = requests.get(url)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            reader = csv.reader(io.StringIO(content))                         # Check if response is successful
            csv_path = f"./meteomatics2/{state}.csv"
            
            with open(csv_path, "w", newline = "") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["date", "max_temp", "min_temp", "pcp"])
                for row in reader:
                    writer.writerow(row)

        else:
            print(f"Error: API request failed with status code {response.status_code}")





        # year = 2022
        # start_time = dt(year, 1, 1)
        # end_time = dt(year, 12)
        # time_step = ":PT1H"
        # parameters_ts = ['t_2m:C', 'rr_1h:mm']
        # loc = (41.664284, -87.486194)
        # format = "JSON"


        # api.query_api()
        
        #url = "https://api.meteomatics.com/"
        #response = requests.get(url, params=params)


    # states = ['ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA', 'COLORADO',          'CONNECTICUT', 'DELAWARE', 'FLORIDA', 'GEORGIA', 'HAWAII', 'IDAHO',          'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS', 'KENTUCKY', 'LOUISIANA',          'MAINE', 'MARYLAND', 'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA',          'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA', 'NEVADA',          'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK',          'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA', 'OREGON',          'PENNSYLVANIA', 'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA',          'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT', 'VIRGINIA', 'WASHINGTON',          'WEST VIRGINIA', 'WISCONSIN', 'WYOMING']
   

if __name__ == "__main__":
    main()


