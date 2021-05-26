import json
from datetime import datetime, timedelta
from sty import fg, bg, rs

from modules.fetch_cryptos import get_by_volume, get_by_increment, get_price


def get_timestamp():
    """Returns formatted string of datetime.now()

    Format: dd/mm/YY hh:mm:ss
    """
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def write_report(convert='USD'):
    """Calls CoinMarketCap API and calculates what today percentile return 
    compared to yesterday if selling 1 unit of top 20 coins by market cap. 
    Writes all retrieved data, timestamp and calculation of JSON file. 

    Arguments: 
        convert (optional): string, (e.g. 'EUR') - defaults to 'USD'

    """

    print(fg.blue + 'Fetching data...' + fg.rs)

    currency_data = {}
    currency_data['timestamp'] = get_timestamp()
    currency_data['converted_in'] = convert
    currency_data['top_by_volume'] = get_by_volume(convert=convert)
    currency_data['top_by_increment'] = get_by_increment(convert=convert)
    currency_data['worst_by_increment'] = get_by_increment(
        order='asc', convert=convert)
    currency_data['total_price_top_20_by_market_cap'] = get_price(
        convert=convert)
    currency_data['total_price_76mln_volume'] = get_price(
        mode='volume', convert=convert)

    print(fg.green + 'Data retrieved successfully - ' + get_timestamp() + fg.rs)
    print(fg.blue + 'Calculating investment returns for today . . .' + fg.rs)

    try:
        yesterday = datetime.today() - timedelta(days=1)
        with open(f"./storage/crypto_data_{yesterday.strftime('%d_%m_%Y')}.json", 'r') as openfile:
            yesterday_data = json.load(openfile)

        initial_value = yesterday_data['total_price_top_20_by_market_cap']
        final_value = currency_data['total_price_top_20_by_market_cap']

        currency_data['today_return'] = str(
            (final_value - initial_value) / initial_value * 100) + " %"

    except FileNotFoundError:
        # The file is the first
        print(fg.red + 'No data ara available for yesterday since this is the first time this bot is running... Skipping return calculations' + fg.rs)
        pass

    with open(f"./storage/crypto_data_{datetime.today().strftime('%d_%m_%Y')}.json", 'w') as outfile:
        json.dump(currency_data, outfile)
