import pandas as pd 
import numpy as np 
import os

from utils import * 

df_2012_summer = pd.DataFrame(pd.read_csv(os.path.join(Y_2012, "summer.csv")))
df_2012_winter = pd.DataFrame(pd.read_csv(os.path.join(Y_2012, "winter.csv")))
df_2012 = pd.concat([df_2012_summer, df_2012_winter])
df_2012 = df_2012.drop('Athlete', axis=1)
df_2016 = pd.DataFrame(pd.read_csv(os.path.join(Y_2016, "athletes.csv")))
df_2020 = pd.DataFrame(pd.read_csv(os.path.join(Y_2020, "athletes.csv")))

print(f'df_2012:\n{df_2012.head()} \n df_2016:\n{df_2016.head()} \n df_2020:\n{df_2020.head()}')