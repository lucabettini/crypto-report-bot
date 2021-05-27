import time
import schedule
from sty import bg, fg, rs


class CryptoBot:
    """Arguments:

            hour: string, format: HH:MM

            convert (optional): string, (e.g. 'EUR') - defaults to 'USD'

        Methods:
            run - calls CoinMarketCap API and saves results to json file
    """

    def __init__(self, report, hour='00:00', convert='USD'):
        self.hour = hour
        self.convert = convert
        self.report = report

    def run(self):

        print(bg.green + fg.black + 'Starting bot - ' +
              self.report.get_timestamp() + fg.rs + bg.rs)

        schedule.every().day.at(self.hour).do(
            lambda: self.report.write_report(convert=self.convert))

        while True:
            schedule.run_pending()
            time.sleep(1)