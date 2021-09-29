'''****************************************************************************
title           : data_parse.py
description     : Kong data from the OpenSea API is parsed with this program
author          : TheBigMort
date_created    : 20210627
date_modified   : 20210929
version         : 2.0
python_version  : 3.9
****************************************************************************'''

def parse_kong_data(kong_dict):

    stat = []
    stat.clear()
    kong_id = kong_dict['token_id']
    owner_address = kong_dict['owner']['address']
    traits = kong_dict['traits']
    sell_orders = kong_dict['sell_orders']
    rarity_url = 'https://rarity.tools/rumble-kong-league/view/{}'.format(kong_id)


    def find_elem(stat):
        try:
            for s in range(len(traits)):
                if traits[s]["trait_type"] == stat:
                    return traits[s]['value']
        except:
            return 'ERROR'
    try:
        last_sale_time = kong_dict['last_sale']['event_timestamp']
    except:
        last_sale_time = ' '
    try:
        last_sale_price = int(kong_dict['last_sale']['total_price'])
        last_sale_price = last_sale_price/1000000000000000000
        last_sale_price = '{} ETH'.format(last_sale_price)
    except:
        last_sale_price = ' '
    try:
        cprice = [a_dict['current_price'] for a_dict in sell_orders]
        current = cprice[0]
        current_price = str(int(current)/1000000000000000000)
        current_price_eth = '{} ETH'.format(current_price)
    except:
        current_price_eth = ' '
    try:
        cdate = [[a_dict['created_date'] for a_dict in sell_orders]]
        list_date = cdate[0][0]
        list_date = list_date.replace('T', ' ')
    except:
        list_date = ' '


    shooting_stat = find_elem('Shooting')
    finish_stat = find_elem('Finish')
    defense_stat = find_elem('Defense')
    vision_stat = find_elem('Vision')

    cumulative_stat = shooting_stat+finish_stat+defense_stat+vision_stat

    result = {'rarity_url': rarity_url,
              'kong_id': kong_id,
              'owner_address': owner_address,
              'num_sales': kong_dict['num_sales'],
              'last_sale_date': last_sale_time[:10],
              'last_sale_price': last_sale_price,
              'list_date': list_date[:19],
              'list_price': current_price_eth,
              'background': find_elem('Background'),
              'fur': find_elem('Fur'),
              'clothes': find_elem('Clothes'),
              'mouth': find_elem('Mouth'),
              'head': find_elem('Head'),
              'head_accessory': find_elem('Head Accessory'),
              'eyes': find_elem('Eyes'),
              'jewellery': find_elem('Jewellery'),
              'shooting': shooting_stat,
              'finish': finish_stat,
              'defense': defense_stat,
              'vision': vision_stat,
              'cumulative': cumulative_stat}
    return result

def parse_sale_data(kong_dict):

    sell_orders = kong_dict['sell_orders']
    kong_id = kong_dict['token_id']


    try:
        last_sale_time = kong_dict['last_sale']['event_timestamp']
        last_sale_price = int(kong_dict['last_sale']['total_price'])
        last_sale_price = last_sale_price / 1000000000000000000
        last_sale_price = '{} ETH'.format(last_sale_price)
    except:
        last_sale_time = ' '
        last_sale_price = ' '
    try:
        cprice = [a_dict['current_price'] for a_dict in sell_orders]
        current = cprice[0]
        current_price = str(int(current)/1000000000000000000)
        current_price_eth = '{} ETH'.format(current_price)
    except:
        current_price_eth = ' '
    try:
        cdate = [[a_dict['created_date'] for a_dict in sell_orders]]
        list_date = cdate[0][0]
        list_date = list_date.replace('T', ' ')
    except:
        list_date = ' '

    result = {'kong_id': kong_id,
              'num_sales': kong_dict['num_sales'],
              'last_sale_date': last_sale_time[:10],
              'last_sale_price': last_sale_price,
              'list_date': list_date[:19],
              'list_price': current_price_eth}

    return result