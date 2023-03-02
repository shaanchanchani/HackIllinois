import requests 
import datetime as dt
import pandas as pd
import requests
import io
import csv
import os

def nceiRequest_populateClimateData(folder_path, dfToPopulate):

    #Input: List of urls to scrape data from
    #Output: Generates csv files within a folder titled "historical" in directory
    def pullData(feature_urls):
        for feature in feature_urls:
            response = requests.get(feature)
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                reader = csv.reader(io.StringIO(content))                       
                csv_path = f"./historical/{feature}.csv"
                with open(csv_path, "w", newline = "") as csv_file:
                    writer = csv.writer(csv_file)
                    for row in reader:
                        writer.writerow(row)


                
    
    pcp = "https://www.ncei.noaa.gov/pub/data/cirs/climdiv/climdiv-pcpnst-v1.0.0-20230206"
    tmax = "https://www.ncei.noaa.gov/pub/data/cirs/climdiv/climdiv-tmaxst-v1.0.0-20230206"
    tmin = "https://www.https://www.ncei.noaa.gov/pub/data/cirs/climdiv/climdiv-tminst-v1.0.0-20230206"

    feature_urls = [pcp,tmax,tmin]

    #pullData(feature_urls)
    dfToPopulate['key'] = dfToPopulate.apply(lambda x: (x['state'], x['year'], x['month']), axis=1)
    #features = ["pcp", "tmax", "tmin"]
    features = ["pcp", "tmax"]

    for feature in features:
        path = os.path.join("./historical",f"{feature}.csv")
        ndf = pd.read_csv(path, delim_whitespace=True, dtype = str)
        ndf.columns = ['id',1,2,3,4,5,6,7,8,9,10,11,12]
        ndf = pd.DataFrame(ndf)
            
        ndf['year'] = ndf['id'].str[-4:]
        ndf['state'] = ndf['id'].astype(str).str[:3]
        ndf = ndf[ndf['year'].astype(int) < 2023]
        ndf = ndf[ndf['year'].astype(int) > 2000]
        ndf = ndf[ndf['state'].astype(int) < 51]
        state_codes = {
            '001': 'Alabama',
            '002': 'Arizona',
            '003': 'Arkansas',
            '004': 'California',
            '005': 'Colorado',
            '006': 'Connecticut',
            '007': 'Delaware',
            '008': 'Florida',
            '009': 'Georgia',
            '010': 'Idaho',
            '011': 'Illinois',
            '012': 'Indiana',
            '013': 'Iowa',
            '014': 'Kansas',
            '015': 'Kentucky',
            '016': 'Louisiana',
            '017': 'Maine',
            '018': 'Maryland',
            '019': 'Massachusetts',
            '020': 'Michigan',
            '021': 'Minnesota',
            '022': 'Mississippi',
            '023': 'Missouri',
            '024': 'Montana',
            '025': 'Nebraska',
            '026': 'Nevada',
            '027': 'New Hampshire',
            '028': 'New Jersey',
            '029': 'New Mexico',
            '030': 'New York',
            '031': 'North Carolina',
            '032': 'North Dakota',
            '033': 'Ohio',
            '034': 'Oklahoma',
            '035': 'Oregon',
            '036': 'Pennsylvania',
            '037': 'Rhode Island',
            '038': 'South Carolina',
            '039': 'South Dakota',
            '040': 'Tennessee',
            '041': 'Texas',
            '042': 'Utah',
            '043': 'Vermont',
            '044': 'Virginia',
            '045': 'Washington',
            '046': 'West Virginia',
            '047': 'Wisconsin',
            '048': 'Wyoming',
            '050': 'Alaska'}
        ndf['state'] = ndf['state'].astype(str).map(state_codes)
        
        swag_df = pd.DataFrame(columns = ['key', f'{feature}'])

        keyList = []
        valList = []

        for index, row in ndf.iterrows():
            for i in range(1,13):
                keyList.append((row['state'], int(row['year']), i))
                valList.append(row[i])

        swag_df['key'] = keyList
        swag_df[f'{feature}'] = valList
        
        dfToPopulate = dfToPopulate.assign(feature = None)

        for index,key in swag_df['key'].items():
            dfToPopulate = dfToPopulate.set_index('key')
            dfToPopulate.loc[dfToPopulate['key']==key,f"{feature}"] = swag_df.loc[index, f"{feature}"]
    return dfToPopulate 

def main():
    pass


if __name__ == "__main__":
    main()