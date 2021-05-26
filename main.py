from modules.CryptoBot import CryptoBot
from modules.CryptoReport import CryptoReport

if __name__ == "__main__":
    report = CryptoReport
    bot = CryptoBot(report=report, hour='23:39', convert='EUR')
    bot.run()
