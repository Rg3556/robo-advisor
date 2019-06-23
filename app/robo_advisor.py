# app/robo_advisor.py

import json
import csv
import os
import datetime

import requests
from dotenv import load_dotenv


load_dotenv() #> loads contents of the .env file into the script's environment


# Formats all prices as USD
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)


#
## INFO INPUTS
#

print("WELCOME TO ROBO ADVISOR!")

selected_stock = input("Please input a stock symbol: ") #> String input


api_key = os.environ.get("ALPHAVANTAGE_API_KEY") # "demo"

# symbol ="MSFT" # TODO: accept user input

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={selected_stock}&apikey={api_key}"
response = requests.get(request_url)
# print(type(response)) #> <class 'requests.models.Response'>
# print(response.status_code) #> 200
# print(response.text) #> string

parsed_response = json.loads(response.text)




#
## Validation
#

try:
    last_refreshed = parsed_response["Meta Data"]['3. Last Refreshed']
    parsed_response['Time Series (Daily)']

except:
    print("-------------------------")
    print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again...")
    print("-------------------------")
    print('Shutting the program down...')
    exit()



#
## Calculation
#

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
recent_low_120 = (recent_low*1.2)





## Request time 
now = datetime.datetime.now()

#
## Recommendation & Reasons (2 ways)
#
# BUY = "Buy"
# reason_buy =  "because the stock's latest closing price is less than 20% above its recent low"
# NOT = "Don't Buy"
# reason_not = "because the stock's latest closing price is more than 20% above its recent low"
# 
# if (float(latest_close) < float(recent_low_120)):
#     recommendation = BUY
#     reason = reason_buy
# else:
#     recommendation = NOT
#     reason = reason_not


def buy_or_not(latest_close,recent_low):
    
    if float(latest_close) < float(recent_low_120):
        return "Buy"
    else:
        return "Don't Buy"
recommendation = buy_or_not(latest_close,recent_low)

def reasons(latest_close,recent_low):
    if float(latest_close) < float(recent_low_120):
        return "because the stock's latest closing price is less than 20% above its recent low"
    else:
        return "because the stock's latest closing price is more than 20% above its recent low"
reason = reasons(latest_close,recent_low)

#A recommendation as to whether or not the client should buy the stock (see guidance below), and optionally 
# what quantity to purchase. The nature of the recommendation for each symbol can be binary (e.g. "Buy" or "No Buy"), 
# qualitative (e.g. a "Low", "Medium", or "High" level of confidence), or quantitative (i.e. some numeric rating scale).
#A recommendation explanation, describing in a human-friendly way the reason why the program produced the 
# recommendation it did (e.g. "because the stock's latest closing price exceeds threshold XYZ, etc...")
# You are free to develop your own custom recommendation algorithm. 
# This is perhaps one of the most fun and creative parts of this project. 
# 😃 One simple example algorithm would be (in pseudocode): 
# If the stock's latest closing price is less than 20% above its recent low, "Buy", else "Don't Buy".




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
    


#
## Challenge of 52-Week Highs and Lows
#
request_url_weekly = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={selected_stock}&apikey={api_key}"
response_weekly = requests.get(request_url_weekly)
parsed_response_weekly = json.loads(response_weekly.text)

tsd_weekly = parsed_response_weekly['Weekly Time Series']
weeks = list(tsd_weekly.keys()) 
weeks_52 = weeks[:52] #> last 52 weeks's data in dynamic
# print(len(weeks_52))
# print(weeks_52)
# breakpoint()

high_weekly_prices = []
low_weekly_prices = []


for week in weeks_52:
    high_weekly_price = tsd_weekly[week]["2. high"]
    high_weekly_prices.append(float(high_weekly_price))
    
    low_weekly_price = tsd_weekly[week]["3. low"]
    low_weekly_prices.append(float(low_weekly_price))

recent_52_week_high = max(high_weekly_prices)
recent_52_week_low = min(low_weekly_prices)



print("-------------------------")
print("SELECTED STOCK SYMBOL: " + str(selected_stock))
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: " +  str(now.strftime("%Y-%m-%d ")) + str(now.strftime("%I:%M %p")))  # + 2019-06-06 11:31 AM
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print(f"RECENT 52-WEEK HIGH: {to_usd(float(recent_52_week_high))}")
print(f"RECENT 52-WEEK LOW: {to_usd(float(recent_52_week_low))}")
print("-------------------------")
print(f"RECOMMENDATION: {str(recommendation)}")
print(f"RECOMMENDATION REASON: {reason}")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path} ...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


