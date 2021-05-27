import time
import schedule
from sty import fg, bg, rs
from modules.crypto_report import write_report, get_timestamp


def crypto_bot(hour='00:00', convert='USD'):
    """Calls CoinMarketCap API and saves results to json file 

    Arguments:

        hour: string, format: HH:MM

        convert (optional): string, (e.g. 'EUR') - defaults to 'USD'
    """

    print(bg.green + fg.black + 'Starting bot - ' +
          get_timestamp() + fg.rs + bg.rs)

    schedule.every().day.at(hour).do(lambda: write_report(convert))

    while True:
        schedule.run_pending()
        time.sleep(1)
