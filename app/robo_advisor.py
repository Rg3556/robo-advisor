# app/robo_advisor.py

import json
import csv
import os
import datetime

import requests
from dotenv import load_dotenv


load_dotenv() #> loads contents of the .env file into the script's environment


def to_usd(my_price):
    return "${0:,.2f}".format(my_price)


#
## INFO INPUTS
#

print("WELCOME TO ROBO ADVISOR!")

selected_stock = input("Please input a stock identifier: ") #> String input


api_key = os.environ.get("ALPHAVANTAGE_API_KEY") # "demo"

symbol ="MSFT" # TODO: accept user input

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={selected_stock}&apikey={api_key}"
response = requests.get(request_url)
# print(type(response)) #> <class 'requests.models.Response'>
# print(response.status_code) #> 200
# print(response.text) #> string

parsed_response = json.loads(response.text)

## Validation

# selected_stock = 0
# selected_stocks = []
# valid_stocks = [str(p["id"]) for p in dict_list] 



try:
    last_refreshed = parsed_response["Meta Data"]['3. Last Refreshed']
    parsed_response['Time Series (Daily)']

except:
    print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again...")
    print('Shutting program down...')
    exit()




tsd = parsed_response['Time Series (Daily)']
dates = list(tsd.keys()) 
latest_day = dates[0] #> make dynamic
latest_close = tsd[latest_day]['4. close']#> $ & string


high_prices = []
low_prices = []



for date in dates:
    high_price = tsd[date]['2. high']
    high_prices.append(float(high_price))
    
    low_price = tsd[date]['3. low']
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)


now = datetime.datetime.now()

#
## INFO OUTPUTS
#
# csv_file_path = "data/prices.csv" # a relative filepath

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp":date,
            "open":daily_prices['1. open'],
            "high":daily_prices['2. high'],
            "low":daily_prices['3. low'],
            "close":daily_prices['4. close'],
            "volume":daily_prices['5. volume']})
    



print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: " +  str(now.strftime("%Y-%m-%d ")) + str(now.strftime("%I:%M %p")))  # + 2019-06-06 11:31 AM
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path} ...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


