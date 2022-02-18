#!/usr/bin/env python3
import pandas as pd
import numpy as np
import cyrtranslit
import sys

df = pd.read_csv(sys.argv[1])
# df = pd.read_csv('unsorted_data/beograd.csv')
len_df = round(len(df)/2)

# sys.argv[3] = 'cyr'
# asa = False

df = df[:len_df]
del df['Stepen1']

if sys.argv[3] == 'lat':
# if asa:
    letters = {
        "Š":"S",
        "Đ":"Dj",
        "Ć":"C",
        "Č":"C",
        "Ž":"Z",
        "š":"s",
        "đ":"dj",
        "ć":"c",
        "č":"c",
        "ž":"z"
    }

    # df['NazivOpstineCyr'] = df['NazivOpstine']
    # df['NazivOkrugaCyr'] = df['NazivOkruga1']
    # df['mernaJedinicaCyr'] = df['mernaJedinica1']
    df['naziv_opstine_clean'] = df['NazivOpstine']
    df['naziv_okruga_clean'] = df['NazivOkruga1']
    labels = df.columns


    for label in labels:
        unique_values = df[label].unique()
        df[label] = df[label].replace(np.nan, 0)
        if label == 'naziv_opstine_clean' or label == 'naziv_okruga_clean':
            for value in unique_values :
                try:
                    value_lat_srb = cyrtranslit.to_latin(value)
                    value_lat = [letters[l] if l in letters.keys() else l for l in value_lat_srb]
                    value_lat = ''.join(value_lat)
                    df[label] = df[label].replace([value], value_lat)
                except:
                    pass

        else:
            for value in unique_values :
                try:
                    df[label] = df[label].replace([value], cyrtranslit.to_latin(value))
                except:
                    pass

    df['NazivOpstineLat'] = df['NazivOpstine']
    df['NazivOkrugaLat'] = df['NazivOkruga1']
    df['mernaJedinica1'] = df['mernaJedinica1'].replace('Hektar, ha ', 'ha')
    df['mernaJedinica1'] = df['mernaJedinica1'].replace('Promil ', '‰')
    df['NazivIndikatora2'] = df[['NazivIndikatora1', 'mernaJedinica1']].agg('/'.join, axis = 1)

    jedinice = df['NazivIndikatora2'].unique().tolist()
    labels_jedinice = dict()

    for j in jedinice:
        a = j.strip().split('/')
        labels_jedinice[a[0]] = a[1]

    df = df.pivot_table(values = 'Vrednost', index = ['naziv_opstine_clean', 'naziv_okruga_clean', 'NazivOpstine', 'NazivOkruga1', 'Datum'], columns = ['NazivIndikatora1'])

elif sys.argv[3] == 'cyr':
# else:
    letters = {
        "Š":"S",
        "Đ":"Dj",
        "Ć":"C",
        "Č":"C",
        "Ž":"Z",
        "š":"s",
        "đ":"dj",
        "ć":"c",
        "č":"c",
        "ž":"z"
    }

    # df['NazivOpstineCyr'] = df['NazivOpstine']
    # df['NazivOkrugaCyr'] = df['NazivOkruga1']
    # df['mernaJedinicaCyr'] = df['mernaJedinica1']
    df['naziv_opstine_clean'] = df['NazivOpstine']
    df['naziv_okruga_clean'] = df['NazivOkruga1']
    labels = df.columns


    for label in labels:
        unique_values = df[label].unique()
        df[label] = df[label].replace(np.nan, 0)
        if label == 'naziv_opstine_clean' or label == 'naziv_okruga_clean':
            for value in unique_values :
                try:
                    value_lat_srb = cyrtranslit.to_latin(value)
                    value_lat = [letters[l] if l in letters.keys() else l for l in value_lat_srb]
                    value_lat = ''.join(value_lat)
                    df[label] = df[label].replace([value], value_lat)
                except:
                    pass

        # else:
        #     for value in unique_values :
        #         try:
        #             df[label] = df[label].replace([value], cyrtranslit.to_latin(value))
        #         except:
        #             pass

    df['NazivOpstineLat'] = df['NazivOpstine']
    df['NazivOkrugaLat'] = df['NazivOkruga1']
    df['mernaJedinica1'] = df['mernaJedinica1'].replace('Хектар, ха ', 'ха')
    df['mernaJedinica1'] = df['mernaJedinica1'].replace('Промил ', '‰')
    df['NazivIndikatora2'] = df[['NazivIndikatora1', 'mernaJedinica1']].agg('/'.join, axis = 1)

    jedinice = df['NazivIndikatora2'].unique().tolist()
    labels_jedinice = dict()

    for j in jedinice:
        a = j.strip().split('/')
        labels_jedinice[a[0]] = a[1]

    df = df.pivot_table(values = 'Vrednost', index = ['naziv_opstine_clean', 'naziv_okruga_clean', 'NazivOpstine', 'NazivOkruga1', 'Datum'], columns = ['NazivIndikatora1'])

new_labels = df.columns
df = df.reset_index()
for label in new_labels:
    column_len = len(df[label])
    df[label] = df[label].astype(str)
    for i in range(column_len):
        value = df.loc[i, [label]].values[0]
        decimals = value.split('.')
        if decimals[1] == '0':
            value = int(decimals[0])
        else:
            value = float(value)
        df.loc[i,[label]] = f'{value} {labels_jedinice[label]}'

    label_lat = cyrtranslit.to_latin(label)
    new_tmp = [letters[l] if l in letters.keys() else l for l in label_lat]
    new = ''.join(new_tmp)
    df = df.rename(columns = {label : new})

# df.to_csv('asa.csv')

df.to_csv(sys.argv[2])
