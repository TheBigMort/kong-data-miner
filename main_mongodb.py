'''
title           : main_mongodb.py
description     : main file for kong_data_miner project
author          : Adil Moujahid
modified_by     : TheBigMort
date_created    : 20210627
date_modified   : 20210929
version         : 2.0
python_version  : 3.9
'''

from data_parse import parse_sale_data
import requests
import time

from pymongo import MongoClient

import matplotlib.pyplot as plt

plt.style.use('ggplot')

# Infinite loop to constantly run and update database
while True:
    # track time to check how long the program takes to run
    start_time = time.time()
    client = MongoClient({MongoDB_DB_Connection_String})
    dbs = client.salesDB
    # these three lines ensure the collection is cleared to prevent duplicate entries
    kongs_sales = dbs.kongsSales
    kongs_sales.drop()
    kongs_sales = dbs.kongsSales

    url = "https://api.opensea.io/api/v1/assets"

    for i in range(0, 334):
        querystring = {"token_ids": list(range((i * 30), (i * 30) + 30)),
                       "asset_contract_address": "0xef0182dc0574cd5874494a120750fd222fdb909a",
                       "order_direction": "desc",
                       "offset": "0",
                       "limit": "50"}
        response = requests.request("GET", url, params=querystring)

        print(i, end=" ")
        if response.status_code != 200:
            print('ERROR, RESPONSE CODE:')
            print(response.status_code)
            break

        # Getting kongs data
        kongs = response.json()['assets']
        # Parsing kongs data
        #parsed_kongs = [parse_kong_data(kong) for kong in kongs]
        parsed_sales = [parse_sale_data(kong) for kong in kongs]
        #storing parsed kongs data into MongoDB
        #kongs_collection.insert_many(parsed_kongs)
        kongs_sales.insert_many(parsed_sales)

    end_time = time.time()
    time_elapsed = end_time - start_time
    print(time_elapsed)
    time.sleep(300)
