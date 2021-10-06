import pandas as pd 
import numpy as np 
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

if __name__ == "__main__":
    print(forecasting())