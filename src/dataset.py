import pandas as pd 
import numpy as np 
import geopandas as gpd
import os

from utils import * 


def forecasting():

    # reading data
    df_2012_summer = pd.DataFrame(pd.read_csv(os.path.join("/kaggle", Y_2012, "summer.csv")))
    df_2012_winter = pd.DataFrame(pd.read_csv(os.path.join("/kaggle", Y_2012, "winter.csv")))
    df_2012 = pd.concat([df_2012_summer, df_2012_winter])
    df_2012 = df_2012.drop('Athlete', axis=1)
    df_2016 = pd.DataFrame(pd.read_csv(os.path.join("/kaggle", Y_2016, "athletes.csv")))
    df_2020 = pd.DataFrame(pd.read_csv(os.path.join("/kaggle", Y_2020, "medals.csv")))

    # 2020 data changes
    df_2020['gold_medal']=df_2020['medal_code'].apply(lambda x: 1 if x==1 else 0)
    df_2020['silver_medal']=df_2020['medal_code'].apply(lambda x: 1 if x==2 else 0)
    df_2020['bronze_medal']=df_2020['medal_code'].apply(lambda x: 1 if x==3 else 0)
    df_2020 = df_2020[['country_code', 'gold_medal', 'silver_medal', 'bronze_medal']]
    df_2020 = df_2020.groupby('country_code').agg(sum)
    df_2020 = df_2020.reset_index(drop=False)
    df_2020.insert(0, 'year', 2020)
    df_2020['total'] = df_2020['gold_medal'] + df_2020['silver_medal'] + df_2020['bronze_medal']

    # 2016 data changes
    df_2016 = df_2016.rename({'nationality': 'country_code', 'gold': 'gold_medal', 'silver': 'silver_medal', 'bronze': 'bronze_medal'}, axis=1)
    df_2016 = df_2016[['country_code', 'gold_medal', 'silver_medal', 'bronze_medal']]
    df_2016 = df_2016.groupby('country_code').agg(sum)
    df_2016 = df_2016.reset_index(drop=False)
    df_2016.insert(0, 'year', 2016)
    df_2016['total'] = df_2016['gold_medal'] + df_2016['silver_medal'] + df_2016['bronze_medal']

    # 2012 data changes
    years = df_2012[df_2012.Year >= 1948].Year.unique()

    df_2012['gold_medal']=df_2012['Medal'].apply(lambda x: 1 if x=='Gold' else 0)
    df_2012['silver_medal']=df_2012['Medal'].apply(lambda x: 1 if x=='Silver' else 0)
    df_2012['bronze_medal']=df_2012['Medal'].apply(lambda x: 1 if x=='Bronze' else 0)
    df_2012 = df_2012.rename({'Country': 'country_code'}, axis=1)
    df_2012 = df_2012[['Year', 'country_code', 'gold_medal', 'silver_medal', 'bronze_medal']]

    df_temp= pd.DataFrame()
    for year in years:
        temp = df_2012[df_2012.Year == year][['country_code', 'gold_medal', 'silver_medal', 'bronze_medal']]
        temp = temp.groupby('country_code').agg(sum)
        temp = temp.reset_index(drop=False)
        temp.insert(0, 'year', year)
        temp['total'] = temp['gold_medal'] + temp['silver_medal'] + temp['bronze_medal']
        df_temp = pd.concat([df_temp, temp])

    # concatinating all the dataframes
    df = pd.concat([df_temp, df_2016, df_2020], axis=0)
    
    return df


def df_for_visualization():

    # print('check1')
    # contains all the border coordinates for each country. 
    url = (
        "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
    )
    country_shapes = f"{url}/world-countries.json"
    global_polygon = gpd.read_file(country_shapes)

    # print('check2')
    # adjusting the 'country_code' to match with country_code of df Dataframe. 
    global_polygon.id =  global_polygon.id.apply(lambda x: 'DEN' if x=='DNK' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'IRI' if x=='IRN' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'NED' if x=='NLD' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'POR' if x=='PRT' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'RSA' if x=='ZAF' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'SUI' if x=='CHE' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'BUL' if x=='BGR' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'GER' if x=='DEU' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'GRE' if x=='GRC' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'MGL' if x=='MNG' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'SLO' if x=='HRV' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'LAT' if x=='LVA' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'NGR' if x=='NGA' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'INA' if x=='IDN' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'PUR' if x=='PRI' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'TTO' if x=='TRI' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'ALG' if x=='DZA' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'PHI' if x=='PHL' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'ZIM' if x=='ZWE' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'CRC' if x=='CRI' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'VIE' if x=='VNM' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'FIJ' if x=='FJI' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'KOS' if x=='-99' else x)
    global_polygon.id =  global_polygon.id.apply(lambda x: 'CRO' if x=='SLO' else x)

    # print('check3')
    # sorting the dataframe by 'gold_medal', 'silver_medal', 'bronze_medal' and 'total'(all years)
    dframe = pd.DataFrame(forecasting())
    temp = dframe.groupby('country_code').agg(sum)
    temp = temp[['gold_medal', 'silver_medal', 'bronze_medal', 'total']]
    temp.head()

    temp = temp.sort_values(['gold_medal', 'silver_medal', 'bronze_medal'], ascending= False)
    temp = temp.reset_index(drop=False)
    
    # print('check4')
    # considering only top 100 countries based on total medals owned till now.
    countries_to_consider = temp['country_code'].head(100)
    countries_to_consider =list(countries_to_consider)
    dframe = dframe[dframe['country_code'].isin(countries_to_consider)]

    # print('check5')
    # Merging the global_polygon and df.
    dframe['id'] = dframe['country_code']
    dframe = dframe.merge(global_polygon, on='id', how='inner')

    # print('check6')
    return dframe, global_polygon

if __name__ == "__main__":
    print(forecasting())
    print(df_for_visualization())