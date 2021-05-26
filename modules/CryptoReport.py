import json
from datetime import datetime, timedelta
from sty import fg, bg, rs

from modules.fetch_cryptos import get_by_volume, get_by_increment, get_price


class CryptoReport:
    def __init__(self, convert='USD'):
        self.convert = convert
        self.currency_data = {}
        self.today_return = 0
        self.start_ts = datetime.now()
        self.active_time = ''

    def get_timestamp(self):
        """Returns formatted string of datetime.now()

        Format: dd/mm/YY hh:mm:ss
        """
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def write_report(self):
        """Calls CoinMarketCap API and calculates what today percentile return 
        compared to yesterday if selling 1 unit of top 20 coins by market cap. 
        Writes all retrieved data, timestamp and calculation of JSON file. 

        Arguments: 
            convert (optional): string, (e.g. 'EUR') - defaults to 'USD'

        """
        print(bg.cyan + fg.black + 'Starting new session - ' +
              self.get_timestamp() + fg.rs + bg.rs)
        print(fg.blue + 'Fetching data...' + fg.rs)

        # Infos about the JSON file
        self.currency_data['timestamp'] = self.get_timestamp()
        self.currency_data['converted_in'] = self.convert

        # Data fetched from the API through helper functions
        self.currency_data['top_by_volume'] = get_by_volume(
            convert=self.convert)
        self.currency_data['top_by_increment'] = get_by_increment(
            convert=self.convert)
        self.currency_data['worst_by_increment'] = get_by_increment(
            order='asc', convert=self.convert)
        self.currency_data['total_price_top_20_by_market_cap'] = get_price(
            convert=self.convert)
        self.currency_data['total_price_76mln_volume'] = get_price(
            mode='volume', convert=self.convert)

        print(fg.green + 'Data retrieved successfully - ' + fg.rs)
        print(fg.blue + 'Calculating investment returns for today . . .' + fg.rs)

        # Calculation of investment returns
        try:
            yesterday = datetime.today() - timedelta(days=1)
            with open(f"./storage/crypto_data_{yesterday.strftime('%d_%m_%Y')}.json", 'r') as openfile:
                yesterday_data = json.load(openfile)

            initial_value = yesterday_data['total_price_top_20_by_market_cap']
            final_value = self.currency_data['total_price_top_20_by_market_cap']
            self.today_return = (
                final_value - initial_value) / initial_value * 100

            self.currency_data['today_return'] = str(self.today_return) + " %"

            # Display result to console
            print(fg.blue + 'Investment return calculated: ' + fg.rs)
            if self.today_return < 0:
                # Bad investment return
                print(
                    fg.yellow + self.currency_data['today_return'] + fg.rs)
                print('Durate, et vosmet rebus servate secundis - Virgil, Aeneid I 207')
            else:
                # Good investment return
                print(fg.green +
                      self.currency_data['today_return'] + fg.rs)
                print('Audentes fortuna iuvat - Virgil, Aeneid X 284')

        except FileNotFoundError:
            # The first time the bot is started, no file with yesterday's data will be available and a
            # FileNotFoundError will be raised. Here we catch it, print a message in console and continue
            print(fg.red + 'No data ara available for yesterday since this is the first time this bot is \
            running... Skipping return calculations' + fg.rs)
            pass

        # Save the data as JSON, with today's date as parte of the file.
        with open(f"./storage/crypto_data_{datetime.today().strftime('%d_%m_%Y')}.json", 'w') as outfile:
            json.dump(self.currency_data, outfile)

        # Display duration in console
        self.active_time = timedelta.total_seconds(
            datetime.now() - self.start_ts)
        print(f"Task completed in {self.active_time} seconds")
        print(fg.blue +
              "Everything done for today, I'm going to sleep" + fg.rs)
