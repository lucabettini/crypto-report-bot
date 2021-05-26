from modules.CryptoBot import CryptoBot

if __name__ == "__main__":
    bot = CryptoBot(hour='19:25', convert='EUR')
    bot.run()
