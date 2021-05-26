import requests
import os

from pydash import _
from sty import fg, bg, rs
from dotenv import load_dotenv

load_dotenv()


def fetch_data(params):
    """Calls CoinMarketCap API with specified params. See https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyListingsLatest for additional infos.

    Arguments: 
        params: dictionary

    Return:
        dictionary (parsed JSON)
    """

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.getenv('API_KEY')
    }
    try:
        # Stops if not receing anything after 10 seconds
        res = requests.get(url=url, headers=headers,
                           params=params, timeout=10)

        if not res.ok:
            # print error message to console, status code and complete URL
            print(bg.red + 'Error:' + bg.rs + '  ' + fg.li_red + res.json()
                  ['status']['error_message'] + fg.rs)
            res.raise_for_status()

        return res.json()['data']

    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

################################


def get_by_volume(convert='USD'):
    """Returns infos about the coin with biggest volume in the last 24 hours. 

    Arguments: 
        convert (optional): string, (e.g. 'EUR') - defaults to 'USD'

    Return:
        dictionary
    """

    params = {
        'start': '1',
        'limit': '10',
        'convert': convert,
        'sort': 'volume_24h'
    }

    crypto = fetch_data(params)[0]

    top_by_volume = {
        'name': _.get(crypto, 'name', None),
        'symbol': _.get(crypto, 'symbol', None),
        'platform': _.get(crypto, 'platform.name', None),
        'volume_24h': crypto['quote'][convert]['volume_24h']
    }
    return top_by_volume


def get_by_increment(convert='USD', order='desc'):
    """Returns infos about the top 10 coins with biggest % increment in the last 24 hours. 

    Arguments: 
        order (optional): string, 'asc' or 'desc' - defaults to 'desc'
        convert (optional): string, (e.g. 'EUR') - defaults to 'USD'

    Return: 
        list of dictionaries
    """

    params = {
        'start': '1',
        'limit': '10',
        'convert': convert,
        'sort': 'percent_change_24h',
        'sort_dir': order
    }

    cryptos = fetch_data(params)

    top_ten = []
    for position, crypto in enumerate(cryptos, start=1):
        data = {
            'position': position,
            'name': _.get(crypto, 'name', None),
            'symbol': _.get(crypto, 'symbol', None),
            'platform': _.get(crypto, 'platform.name', None),
            'percent_change_24h': crypto['quote'][convert]['percent_change_24h']
        }
        top_ten.append(data)

    return top_ten


def get_price(convert='USD', mode='marketCap', minVolume=76000000):
    """Returns infos about the total price of a variable number of cryptos depending on the specified parameters. 
    If mode is set to 'marketCap', the total price is the sum of top 20 cryptos by market cap. 
    If mode is set to 'volume', the total price is the sum of the top 100 cryptos by market cap with a volume 
    greather than the one specified. 

    Arguments: 
        mode: string: 'marketCap' or 'volume'
        minVolume (only if mode='volume'): integer - defaults to 76000000
        convert (optional): string, (e.g. 'EUR') - defaults to 'USD'

    Return: 
        list of dictionaries
    """

    params = {
        'start': '1',
        'convert': convert
    }

    if mode == 'marketCap':
        params['limit'] = '20'
    elif mode == 'volume':
        params['volume_24h_min'] = minVolume

    cryptos = fetch_data(params)

    total_price = 0
    for crypto in cryptos:
        total_price += crypto['quote'][convert]['price']

    return total_price
