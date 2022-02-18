#!/usr/bin/env python3
import os
import pandas as pd
from sql import sql_execute
import sqlite3
import sys
import re


df = pd.read_csv(sys.argv[2])

df = df.iloc[:, 1:]
old_labels = df.columns.tolist()[1:]
gradovi_lat = list()
gradovi_cyr = list()


for label in old_labels[:4]:
    column_len = len(df[label])
    for i in range(column_len):
        final_value = str()
        value = df.loc[i, [label]].values[0]
        values_tmp = value.split('-')
        values = [v.strip() for v in values_tmp if v]
        final_value = ' '.join(values)

        df.loc[i,[label]] = final_value

labels_tmp = df.columns.tolist()[6:]
first_labels = df.columns.tolist()[1:6]
first_labels[0] = 'naziv_opstine_clean'
first_labels[1] = 'naziv_okruga_clean'
first_labels[2] = 'naziv_opstine'
first_labels[3] = 'naziv_okruga'
first_labels[4] = 'godina'

labels = [label[4:].strip().lower().replace(' ' , '_') for label in labels_tmp]
true_labels = first_labels + labels

table_fields = str()

for label in true_labels:
    if label == true_labels[-1]:
        label = label.replace(',', '')
        field = f'"{label}" TEXT'
    else:
        label = label.replace(',', '')
        field = f'"{label}" TEXT, '

    table_fields += field

df_len = len(df)

if sys.argv[1] == 'load':
    jedinice = ['Broj', 'Odnos', 'Indeks', 'Koeficijent', 'Број', 'Однос', 'Индекс', 'Коефицијент']
    for j in range(len(df)):
        values1 = str()
        for i in range(len(old_labels)):
            if i > 4:
                value, measurment = str(df.loc[j, [old_labels[i]]].values[0]).split(' ')
                if measurment not in jedinice:
                    value += f' {measurment}'
            else:
                value = df.loc[j, [old_labels[i]]].values[0]

            if i == len(old_labels) - 1:
                values1 += f'"{value}"'
            else:
                values1 += f'"{value}", '


        if sys.argv[3] == 'lat':
            sql = f'INSERT INTO opstine_lat VALUES({j}, {values1})'
            sql_execute(sql, 'change')
        elif sys.argv[3] == 'cyr':
            sql = f'INSERT INTO opstine_cyr VALUES({j}, {values1})'
            sql_execute(sql, 'change')
        os.system('clear')
        percent = round((j / df_len) * 100,2)
        print(f'{percent} %')

elif sys.argv[1] == 'create':
    if sys.argv[3] == 'lat':
        sql = f'CREATE TABLE opstine_lat("opstina_id" INTEGER NOT NULL PRIMARY KEY, {table_fields})'
        sql_execute(sql, 'change')
    elif sys.argv[3] == 'cyr':
        sql = f'CREATE TABLE opstine_cyr("opstina_id" INTEGER NOT NULL PRIMARY KEY, {table_fields})'
        sql_execute(sql, 'change')
