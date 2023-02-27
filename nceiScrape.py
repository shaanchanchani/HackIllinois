import requests 

import datetime as dt
import meteomatics.api as api
import pandas as pd
import requests
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


    for state in states:
        location = geolocator.geocode(state, exactly_one=True)
        locations.append((location.latitude, location.longitude))
        url = f"https://api.meteomatics.com/{startdate_ts}--{enddate_ts}:PT1H/t_max_2m_24h:F,t_min_2m_24h:F,precip_24h:mm/{str(location.latitude)},{str(location.longitude)}/csv?access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJ2IjoxLCJ1c2VyIjoicHVyZHVlX2NoYW5jaGFuaSIsImlzcyI6ImxvZ2luLm1ldGVvbWF0aWNzLmNvbSIsImV4cCI6MTY3NzM5MjE5Niwic3ViIjoiYWNjZXNzIn0.2hwOgmatPIMBuWUnAfy4UJrcXHdz87jCVU2zsi3iLy6EUPvEUKIjkLayuojJtgWPYZF05Q55l3Td2Go-jLApfQ"

        response = requests.get(url)