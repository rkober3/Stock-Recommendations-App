#Stock Advisor Application


from   dotenv import load_dotenv
import json
import os
import csv
import requests
from   IPython import embed
from   statistics import mean
import datetime


load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

def parse_response(all_stock_info):
    # response_text can be either a raw JSON string or an already-converted dictionary
    if isinstance(all_stock_info, str): # if not yet converted, then:
        all_stock_info = json.loads(all_stock_info) # convert string to dictionary

    results = []
    time_series_daily = all_stock_info["Time Series (Daily)"] #> a nested dictionary
    for trading_date in time_series_daily: # FYI: can loop through a dictionary's top-level keys/attributes
        prices = time_series_daily[trading_date] #> {'1. open': '101.0924', '2. high': '101.9500', '3. low': '100.5400', '4. close': '101.6300', '5. volume': '22165128'}
        result = {
            "date": trading_date,
            "open": prices["1. open"],
            "high": prices["2. high"],
            "low": prices["3. low"],
            "close": prices["4. close"],
            "volume": prices["5. volume"]
        }
        results.append(result)
    return results

def write_prices_to_file(prices, filename):
    csv_filepath = os.path.join(os.path.dirname(__file__), "data", filename)
    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        for d in prices:
            row = {
                "timestamp": d["date"], # change attribute name to match project requirements
                "open": d["open"],
                "high": d["high"],
                "low": d["low"],
                "close": d["close"],
                "volume": d["volume"]
            }
            writer.writerow(row)

# see: https://www.alphavantage.co/support/#api-key
api_key = os.environ.get("ALPHAVANTAGE_API_KEY") or "OOPS. Please set an environment variable named 'ALPHAVANTAGE_API_KEY'."

symbol = input("Please enter a stock symbol:").upper()

try:
        float(symbol)
        quit("CHECK YOUR SYMBOL. EXPECTING A NON-NUMERIC SYMBOL")
except ValueError as e:
    pass

#https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo
request_url = str("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+symbol+"&apikey="+api_key)

response = requests.get(request_url)

if "Error" in response.text:
    print("Stock symbol not valid")
    quit("Stopping the program")
all_stock_info = json.loads(response.text)
stock_info = all_stock_info["Time Series (Daily)"]
todays_price = stock_info[str(datetime.datetime.today()).split()[0]]
last_price = todays_price["4. close"]

file_name = str("prices_"+symbol+".csv")

prices = parse_response(all_stock_info)

write_prices_to_file(prices, file_name)

now = datetime.datetime.now()
print("Run at: "+now.strftime("%H:%M")+" on "+now.strftime("%m-%d-%Y"))

print("Price at last close for "+symbol+": "+"${0:.2f}".format(float(last_price)))
high = []
for p in prices:
    high.append(float(p["high"]))

low = []
for p in prices:
    low.append(float(p["low"]))

print("The recent average high price for "+symbol+" is: "+"${0:.2f}".format(float(mean(high))))
print("The recent average low price for "+symbol+" is: "+"${0:.2f}".format(float(mean(low))))

close = []
for p in prices:
    close.append(float(p["close"]))

sma100 = sum(close)/len(close)

if sma100 <= close[0]:
    print(symbol+" is trading above its 100-day simple moving average. The stock is a buy!")
else:
    print("Unfortunately, "+symbol+" is trading below its 100-day simple moving average. SELL NOW!")


dates = []
for d in prices:
    dates.append(d["date"])

print("Latest data from: "+dates[0])
