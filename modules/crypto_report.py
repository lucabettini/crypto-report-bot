import json
from datetime import datetime, timedelta
from sty import fg, bg, rs

from modules.fetch_cryptos import get_by_volume, get_by_increment, get_price


def get_timestamp():
    """Returns formatted string of datetime.now()

    Format: dd/mm/YY hh:mm:ss
    """
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def prepare_report(convert='USD'):
    """Prints starting timestamps

    Arguments: 
        convert (optional): string, (e.g. 'EUR') - defaults to 'USD'
    Return:
        dictionary: { timestamp, convert }
    """

    print('***************************************')
    print(bg.cyan + fg.black + 'Starting new session - ' +
          get_timestamp() + fg.rs + bg.rs)
    print(fg.blue + 'Fetching data...' + fg.rs)

    # Infos about the JSON file
    return {
        'timestamp': get_timestamp(),
        'converted_in': convert
    }


def fetchData(convert='USD'):
    """Fetches data from CoinMarketCap API.
    Arguments: 
        convert (optional): string, (e.g. 'EUR') - defaults to 'USD'
    Return:
        dictionary
    """

    # Data fetched from the API through helper functions
    return {
        'top_by_volume': get_by_volume(convert=convert),
        'top_by_increment': get_by_increment(convert=convert),
        'worst_by_increment': get_by_increment(
            order='asc', convert=convert),
        'total_price_top_20_by_market_cap': get_price(
            convert=convert),
        'total_price_76mln_volume': get_price(
            mode='volume', convert=convert)
    }


def calculateReturns(total_price):
    """Calculates what today percentile return compared to yesterday if selling 
            1 unit of top 20 coins by market cap. 
    Arguments: 
        total_price: integer
    Return:
        dictionary
    """

    print(fg.blue + 'Calculating investment returns for today . . .' + fg.rs)

    # Calculation of investment returns
    try:
        yesterday = datetime.today() - timedelta(days=1)
        with open(f"./storage/crypto_data_{yesterday.strftime('%d_%m_%Y')}.json", 'r') as openfile:
            yesterday_data = json.load(openfile)

        initial_value = yesterday_data['total_price_top_20_by_market_cap']
        final_value = total_price
        today_return_integer = (
            final_value - initial_value) / initial_value * 100

        today_return = str(today_return_integer) + " %"

        # Display result to console
        print(fg.blue + 'Investment return calculated: ' + fg.rs)
        if today_return_integer < 0:
            # Bad investment return
            print(
                fg.yellow + today_return + fg.rs)
            print('Durate, et vosmet rebus servate secundis - Virgil, Aeneid I 207')
        else:
            # Good investment return
            print(fg.green +
                  today_return + fg.rs)
            print('Audentes fortuna iuvat - Virgil, Aeneid X 284')

        return {
            'today_return': today_return
        }

    except FileNotFoundError:
        # The first time the bot is started, no file with yesterday's data will be available and a
        # FileNotFoundError will be raised. Here we catch it, print a message in console and continue
        print(fg.red + 'No data ara available for yesterday since this is the first time this bot is \
        running... Skipping return calculations' + fg.rs)
        pass


def display_duration(timestamp):
    """Displays duration of operations in console, comparing datetime.now() with provided timestamp
    and prints message in console. 
    Arguments: 
        timestamp: datetime object
    """
    active_time = timedelta.total_seconds(datetime.now() - timestamp)
    print(f"Task completed in {active_time} seconds")
    print(fg.blue +
          "Everything done for today, I'm going to sleep" + fg.rs)


def write_report(convert='USD'):
    """Calls CoinMarketCap API, calculates investment returns and writes fetched data, result and timestamp in a JSON file. 
        Arguments: 
            convert (optional): string, (e.g. 'EUR') - defaults to 'USD'

    """
    start_ts = datetime.now()

    fetched_data = {**prepare_report(convert), **fetchData(convert)}
    print(fg.green + 'Data retrieved successfully - ' + get_timestamp() + fg.rs)

    currency_data = {**fetched_data, **
                     calculateReturns(fetched_data['total_price_top_20_by_market_cap'])}

    # Save the data as JSON, with today's date as parte of the file.
    with open(f"./storage/crypto_data_{datetime.today().strftime('%d_%m_%Y')}.json", 'w') as outfile:
        json.dump(currency_data, outfile)

    display_duration(start_ts)
