import time
import schedule
from sty import bg, fg, rs
from modules.CryptoReport import CryptoReport


class CryptoBot:
    """Arguments:

            hour: string, format: HH:MM

            convert (optional): string, (e.g. 'EUR') - defaults to 'USD'

        Methods:
            run - calls CoinMarketCap API and saves results to json file
    """

    def __init__(self, hour='00:00', convert='USD'):
        self.hour = hour
        self.convert = convert

    def run(self):
        report = CryptoReport(self.convert)

        print(bg.green + fg.black + 'Starting bot - ' +
              report.get_timestamp() + fg.rs + bg.rs)

        schedule.every().day.at(self.hour).do(lambda: report.write_report())

        while True:
            schedule.run_pending()
            time.sleep(1)
