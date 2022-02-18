import pandas as pd
from os import listdir

data_files = listdir('sorted_data')
df_lat = list()
df_cyr = list()

for file in data_files:
    path = f'sorted_data/{file}'
    df_tmp = pd.read_csv(path)
    if 'lat' in path:
        df_lat.append(df_tmp)
    elif 'cyr' in path:
        df_cyr.append(df_tmp)

df_lat = pd.concat(df_lat, ignore_index = True)
df_cyr = pd.concat(df_cyr, ignore_index = True)


df_lat.to_csv('all_data_lat.csv')
df_cyr.to_csv('all_data_cyr.csv')

