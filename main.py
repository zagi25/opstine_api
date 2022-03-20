#!/usr/bin/env python3
import socket
import os
import uvicorn
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from response import Response


HOST = socket.gethostbyname(socket.gethostname())
PORT = int(os.environ.get("PORT", 5000))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_methods = ['GET'],
    allow_headers = ['*']
)

@app.get('/get_data')
async def get_data(opstina: Optional[str] = None, okrug: Optional[str] = None, podaci: Optional[str] = 'sve', godina: Optional[str] = '2020', pismo: Optional[str] = 'lat'):
    args = locals()
    conditions = str()
    select = str()
    for key in args.keys():
        if args[key]:
            if args[key] == opstina:
                opstine = opstina.split(',')
                if len(opstine) == 1:
                    opstina = opstina.replace('_', ' ')
                    conditions += f'naziv_opstine_clean="{opstina}" AND '
                else:
                    sve_opstine = str()
                    for ops in opstine:
                        if ops != opstine[-1]:
                            sve_opstine += f'"{ops}", '
                        else:
                            sve_opstine += f'"{ops}"'
                    conditions += f'naziv_opstine_clean IN ({sve_opstine}) AND '

            elif args[key] == okrug:
                okruzi = okrug.split(',')
                if len(okruzi) == 1:
                    okrug = okrug.replace('-', ' ')
                    conditions += f'naziv_okruga_clean="{okrug}" AND '
                else:
                    svi_okruzi = str()
                    for okr in okruzi:
                        if okr != okruzi[-1]:
                            svi_okruzi += f'"{okr}", '
                        else:
                            svi_okruzi += f'"{okr}"'
                    conditions += f'naziv_okruga_clean IN ({svi_okruzi}) AND '

            elif args[key] == podaci:
                if podaci == 'sve':
                    select = '*'
                else:
                    select = f'naziv_opstine, naziv_okruga, godina, {podaci}'

            elif args[key] == godina:
                if len(godina) == 4:
                    conditions += f'godina="{godina}"'
                else:
                    godine = godina.split('-')
                    sve_godine = [str(godina) for godina in range(int(godine[0]), int(godine[1])+1)]
                    sve_godine = ','.join(sve_godine)
                    conditions += f'godina IN ({sve_godine})'

    if pismo == 'lat':
        sql = f'SELECT {select} FROM opstine_lat WHERE {conditions}'
    elif pismo == 'cyr':
        sql = f'SELECT {select} FROM opstine_cyr WHERE {conditions}'
    res = Response(sql_string = sql, get = 'podaci')

    return res.getResponse()

@app.get('/godine')
async def get_godine():
    sql = f'SELECT DISTINCT godina FROM opstine_lat'
    res = Response(sql, get = 'godine')

    return res.getResponse()

@app.get('/opstine')
async def get_opstine(pismo: Optional[str] = 'lat'):
    sql = str()
    if pismo == 'lat':
        sql = f'SELECT DISTINCT naziv_opstine FROM opstine_lat'
    elif pismo == 'cyr':
        sql = f'SELECT DISTINCT naziv_opstine FROM opstine_cyr'

    res = Response(sql, get = 'opstine')

    return res.getResponse()

@app.get('/okruzi')
async def get_okgruzi(pismo: Optional[str] = 'lat'):
    sql = str()
    if pismo == 'lat':
        sql = f'SELECT DISTINCT naziv_okruga FROM opstine_lat'
    elif pismo == 'cyr':
        sql = f'SELECT DISTINCT naziv_okruga FROM opstine_cyr'

    res = Response(sql, get = 'okruzi')

    return res.getResponse()

@app.get('/podaci')
async def get_podaci():
    sql = 'PRAGMA table_info(opstine_lat)'
    res = Response(sql, get = 'tipovi_podataka')

    return res.getResponse()


if __name__ == "__main__":
    uvicorn.run("main:app", host = HOST, port = 8000)
