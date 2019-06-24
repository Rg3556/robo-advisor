# app/robo_advisor.py

import json
import csv
import os
import datetime
import pandas 
import matplotlib.pyplot as plt

import requests
from dotenv import load_dotenv
import pprint
from twilio.rest import Client
import sendgrid
from sendgrid.helpers.mail import * # source of Email, Content, Mail, etc.


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

# Preliminary validations
if len(selected_stock) < 5 and selected_stock.isupper()==True:
    print("-------------------------")
else:
    
    print("-------------------------")
    print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again...")
    print('Shutting the program down...')
    exit()

     
# HTTP request validations
try:
    last_refreshed = parsed_response["Meta Data"]['3. Last Refreshed']
    parsed_response['Time Series (Daily)']
except:
    print("-------------------------")
    print("Sorry, couldn't find any trading data for that stock symbol. Please try again with a properly-formed stock symbol, like 'MSFT'...")
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
print("-------------------------")
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


#
## Challenge of Plotting Prices over Time
# 
# 
# 
stock_prices = "prices.csv"

csv_filepath = os.path.join("data", stock_prices)

prices = pandas.read_csv(csv_filepath)


Time = prices ["timestamp"]
cp = prices["close"]
hp = prices ["high"]
lp = prices ["low"]
op = prices ["open"]
plt.plot(Time,cp, color='g', label="Closing prices")
plt.plot(Time,hp, color='r', label="High prices")
plt.plot(Time,lp, color='b', label="Low prices")
plt.plot(Time,op, color='y', label="Open prices")
plt.xlabel('Time')
plt.ylabel('Prices')
plt.title('Stock Prices Over Time')
plt.style.use('seaborn-darkgrid')
plt.legend()
plt.show()




#
## Challenge of Sending Alerts via Email/SMS
#

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "OOPS, please specify env var called 'TWILIO_ACCOUNT_SID'")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", "OOPS, please specify env var called 'TWILIO_AUTH_TOKEN'")
SENDER_SMS  = os.environ.get("SENDER_SMS", "OOPS, please specify env var called 'SENDER_SMS'")
RECIPIENT_SMS  = os.environ.get("RECIPIENT_SMS", "OOPS, please specify env var called 'RECIPIENT_SMS'")

# AUTHENTICATE

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# COMPILE REQUEST PARAMETERS (PREPARE THE MESSAGE)

content = "Price Movement Alert! Your selected stock's price has changed by more than 5% within the past day"

# ISSUE REQUEST (SEND SMS)
the_last_day = dates[1] #> make dynamic
the_last_close = tsd[the_last_day]['4. close']#> $ & string
alert_change = float(the_last_close)*0.05

if abs(float(latest_close) - float(the_last_close)) > alert_change :
    message = client.messages.create(to=RECIPIENT_SMS, from_=SENDER_SMS, body=content)
else:
    exit()

# PARSE RESPONSE

pp = pprint.PrettyPrinter(indent=4)

print("----------------------")
print("SMS")
print("----------------------")
print("RESPONSE: ", type(message))
print("FROM:", message.from_)
print("TO:", message.to)
print("BODY:", message.body)
print("PROPERTIES:")
pp.pprint(dict(message._properties))



SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
MY_EMAIL_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")

# AUTHENTICATE

sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

# COMPILE REQUEST PARAMETERS (PREPARE THE EMAIL)

from_email = Email(MY_EMAIL_ADDRESS)
to_email = Email(MY_EMAIL_ADDRESS)
subject = "Price Movement Alert!"
message_text = "Hello, \n\nYour selected stock's price has changed by more than 5% within the past day!\n\nYou can make your investment decisions based on our recommendation.\n\nHappy investing\n\n--Robo Advisor! "
content = Content("text/plain", message_text)
mail = Mail(from_email, subject, to_email, content)

# ISSUE REQUEST (SEND EMAIL)
if abs(float(latest_close) - float(the_last_close)) > alert_change :
    response = sg.client.mail.send.post(request_body=mail.get())
else:
    exit()
# PARSE RESPONSE

pp = pprint.PrettyPrinter(indent=4)

print("----------------------")
print("EMAIL")
print("----------------------")
print("RESPONSE: ", type(response))
print("STATUS:", response.status_code) #> 202 means success
print("HEADERS:")
pp.pprint(dict(response.headers))
print("BODY:")
print(response.body) #> this might be empty. it's ok.)
