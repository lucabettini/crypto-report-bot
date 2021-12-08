![crypto report bot image](https://lucabettini.com/images/cryptobot.png)

# CRYPTO REPORT BOT

<i>Completed on May 27, 2021</i>

This is a simple bot created as a personal project - the first using Python - while following the [Start2Impact](https://www.start2impact.it/) blockchain development course.

The requirements were:

- The bot must start every day at a specific hour
- The bot must fetch the following data from CoinMarketCap API:
  - The cryptocurrency with the greatest 24h volume
  - The best 10 criptocurrencies by 24h percentile increment
  - The worst 10 criptocurrencies by 24h percentile increment
  - The amount required to buy 1 unit of every first 20 cryptocurrencies by market capitalization
  - The amount required to buy 1 unit of every cryptocurrency which 24h volume is greather than 76.000.000$
  - The % of returns realized buy selling today 1 unit of the best 20 cryptocurrencies by market cap, assuming they were acquired the day before and the list has not changed.
- All results must be saved in a JSON file
- The bot must be built with Python 3+

<br>

**Your are in the OOP branch, built with an object-oriented approach. An alternative, more functional approach, is available in [the main branch](https://github.com/lucabettini/crypto-report-bot)**

<br>

## DESCRIPTION

The core modules are inside the /modules folder and consist of three .py files.

In [fetch_cryptos](https://github.com/lucabettini/crypto-report-bot/blob/OOP/modules/fetch_cryptos.py) I have defined three helper functions that make different calls to the API according to the specified parameters: one for retrieving the crypto with the greatest volume, another for the list of cryptos with the best or worst 24h increment and a final one to calculate the amount required to buy 1 unit of a certain stack of cryptos.
All of them call the simple fetch_data function in that same module, which actually performs the request to the server. I've used [pydash](https://pypi.org/project/pydash/) to easily extract values from the API even when some fields are null.

In [CryptoReport](https://github.com/lucabettini/crypto-report-bot/blob/OOP/modules/CryptoReport.py), a dictionary called currency_data is built by calling a series of methods, which: - Add the timestamp and the currency used for conversion - Add all the data fetched using the helper functions of [fetch_cryptos](https://github.com/lucabettini/crypto-report-bot/blob/OOP/modules/fetch_cryptos.py) - Add the calculated investment return, if possible.
The dictionary is then converted into JSON and saved.

Inside [CryptoBot](https://github.com/lucabettini/crypto-report-bot/blob/OOP/modules/CryptoBot.py) an instance of CryptoReport class is passed as a parameter, decoupling the two classes (this is one of the main difference with the main branch) and executed using the [schedule](https://pypi.org/project/schedule/) package. This class is the one instantiated in main.py with the relative parameters.

The bot has a convert parameter, which sets the fiat currency used for conversion. Since the results of the return calculation would be altered if we compared yesterday and today's prices in two different currencies, I've added a simple custom exception inside [crypto_report](https://github.com/lucabettini/crypto-report-bot/blob/main/modules/crypto_report.py).

In the same vein, I've also added an except for FileNotFoundError, to prevent from calculating the returns during the bot first cycle. I realise that this is not a very elegant nor scalable solution, but since this is a very small application that's not designed for scalability, I've decided to keep it that way instead of implementing a counter that would have been more complex than the application itself. This way, contents inside the folder may be deleted completely or the bot can be stopped and run again without difficulties.

Finally, to make the usage more appealing, I've used the [sty package](https://pypi.org/project/sty/) to add some colors to all the messages in console.

<br>

## USAGE

Make sure to have Python 3.9 and pipenv installed.

Install the required dependencies:

    pipenv install

Activate the virtual shell:

    pipenv shell

Get your CoinMarketCap API key [here](https://coinmarketcap.com/api/). Then create a .env in the root directory, with this syntax:

    API_KEY=*your_api_key_here*

Open main.py, adjust the parameters to your liking, and start the bot by running:

    python main.py

<br>

---

Made by [Luca Bettini](https://lucabettini.github.io/).
