import pandas as pd
import os
import requests
import json
import csv
import io
from nassRequest import nassRequest_pr
from nceiRequest import nceiRequest_populateClimateData


def main():
    df_price = nassRequest_pr("./pr")
    df = nceiRequest_populateClimateData("./historical",df_price)
    print(df.head())




if __name__ == "__main__":
    main()