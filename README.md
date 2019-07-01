# Robo-advisor Project

## Prerequisites ##
- Anaconda 3.7    
- Python 3.7
- Pip


## Setup ##

### Repo Setup/Installation

Visit the source code repository for the Rg3556's robo-advisor project [github source] (https://github.com/Rg3556/robo-advisor) and click "Fork" to copy the repo under your own control.

Then download (or "clone") your copy of the repo onto your local computer using GitHub Desktop or the command-line. Choose a familiar download location like the Desktop.
    
    https://github.com/Rg3556/robo-advisor.git # this is the HTTP address, but you could alternatively use the SSH address
    

Then use your command line application (Mac Terminal or Windows Git Bash) to navigate to the location where you downloaded this repo.

    cd ~/Desktop/robo-advisor


Open the repo with your text editor (VS Code), and follow the instruction of the repo's "README.md" file to do the following setup.



### Environment Setup

Create and activate a new Anaconda virtual environment:

    
    conda create -n stocks-env python=3.7 # (first time only)
    conda activate stocks-env
    

From within the virtual environment, install Python package dependencies:

NOTE: we won't need pytest until/unless addressing the optional "Automated Testing" challenge,so you can feel free to skip this now and return later...

    
    pip install requests
    pip install python-dotenv
    pip install pandas
    pip install matplotlib #(for the line plot)
    pip install -r requirements.txt #> (loads contents of the .env file into the script's environment, and for Mail and SMS messages)
    pip install pytest # (only if you'll be writing tests)
    

### AlphaVantage API Setup
This program will need an API Key to issue requests to the AlphaVantage API to retrieve corresponding stock market data. To request to the AlphaVantage API, go to https://www.alphavantage.co/ and get a free API key. Replace your API key to the environment variable called ALPHAVANTAGE_API_KEY in a file called ".env".
    
    ALPHAVANTAGE_API_KEY="YOUR_API_KEY"
    

### Sendgrid Setup

To get receipt via emial, sign up for a Sendgrid free account:https://signup.sendgrid.com/, then click the link in a confirmation email to verify your account. Then create an API Key with "full access" permissions: https://app.sendgrid.com/settings/api_keys.

Update the contents of the ".env" file and replace the API Key value in an environment variable called SENDGRID_API_KEY. Also set and replace with an environment variable called MY_EMAIL_ADDRESS to be the email address you just associated with your SendGrid account (e.g. "abc123@gmail.com").

From within the virtual environment, install the sendgrid package:
    
    pip install sendgrid == 6.0.5


### SMS Setup

For SMS capabilities, sign up for a Twilio account (https://www.twilio.com/try-twilio), click the link in a confirmation email to verify your account, then confirm a code sent to your phone to enable 2FA.

Then create a new project (https://www.twilio.com/console/projects/create) with "Programmable SMS" capabilities. And from the console, view that project's Account SID and Auth Token. Update the contents of the ".env" file to specify these values as environment variables called TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN, respectively.

You'll also need to obtain a Twilio phone number to send the messages from (https://www.twilio.com/console/sms/getting-started/build). After doing so, update the contents of the ".env" file to specify this value (including the plus sign at the beginning) as an environment variable called SENDER_SMS.

Finally, set an environment variable called RECIPIENT_SMS to specify the recipient's phone number (including the plus sign at the beginning).

From within the virtual environment, install the twilio package:
    
    pip install twilio


## Usage ##

From within the virtual environment, demonstrate your ability to run the Python script from the command-line:

    python robo_advisor.py


From the output, you will get:
- The selected stock symbol(s) (e.g. "Stock: MSFT").
- The date and time when the program was executed.
- The date when the data was last refreshed.
- A csv file with the selected stock data you acquired from the website.
- The stock's latest closing price, its recent high price, its recent low price, its recent 52-week high price,a nd its recent 52-week low price.
- A recommendation as to whether or not the client should buy the stock and a recomendation explanation
- A line graph of the stock price changes over time.
- Both email and SMS alert if the selected srock's latest price movement is more than 5% within the past day







