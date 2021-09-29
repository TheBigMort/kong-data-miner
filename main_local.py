'''****************************************************************************
title           : main_local.py
description     : main file for kong_data_miner project
author          : Adil Moujahid
modified_by     : TheBigMort
date_created    : 20210627
date_modified   : 20210929
version         : 2.0
python_version  : 3.9
****************************************************************************'''

from data_parse import parse_kong_data
import requests
import time
import pandas as pd

csv_data_file = "kongs_data.csv"

# Infinite loop to constantly run and update database
while True:

    # track time to check how long the program takes to run
    start_time = time.time()
    df = pd.DataFrame()
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

        # Get kongs data
        kongs = response.json()['assets']
        # Parse kongs data
        parsed_kongs = [parse_kong_data(kong) for kong in kongs]
        # insert data into kong_data
        df = df.append(parsed_kongs, ignore_index=True)

    # create csv file with kongs data
    df.to_csv(csv_data_file, header=True)

    # calculate and print total program run time 
    end_time = time.time()
    time_elapsed = end_time - start_time
    print(time_elapsed)
    time.sleep(300)
