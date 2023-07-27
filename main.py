from twilio.rest import Client
from datetime import datetime
import requests
import chardet
import urllib3
import json
import os

# DECLARE CONSTANTS
CRYPTO_SYMBOL = "BTC"
CRYPTO_NAME = "bitcoin"
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

# DATE_BEFORE_YESTERDAY = datetime.now().strftime("%Y-%m-%d")
# DATE_YESTERDAY = datetime.now().strftime("%Y-%m-%d")

STOCK_API_KEY = "your_stock_data_api_key"
NEWS_API_KEY = "your_news_api_key"
# Twilio to send sms
TWILIO_API_KEY = "your_twilio_api_key"
TWILIO_APP_ID = "your_twilio_app_id"

# TWILIO_APP_ID = os.environ['TWILIO_ACCOUNT_SID']
# TWILIO_API_KEY = os.environ['TWILIO_AUTH_TOKEN']

# To get stock data
STOCK_ENDPOINT = "https://www.alphavantage.co/query?"
# To get news data
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_PARAMS = {
    'function':'TIME_SERIES_DAILY',
    'symbol':STOCK_NAME,
    'apikey':STOCK_API_KEY,
}

NEWS_PARAMS = {
    'q':COMPANY_NAME,
    'searchIn':'title',
    'apiKey':NEWS_API_KEY,
    'language': 'en'
}

CRYPTO_PARAMS = {
    'function':'DIGITAL_CURRENCY_DAILY',
    'symbol': CRYPTO_SYMBOL,
    'market':'USD',
    'apiKey':STOCK_API_KEY,
}

# Get Stock data using request library. For crypto data replace STOCK_PARAMS WITH CRYPTO_PARAMS
r = requests.get(url= STOCK_ENDPOINT, params= STOCK_PARAMS)
data = r.json()['Time Series (Daily)']
# print(data)
data_list = [price for (date, price) in data.items()]

# Get yesterday's closing stock price.
yesterday_data = float(data_list[0]['4. close'])

# Get the day before yesterday's closing stock price
day_before_yesterday_data = float(data_list[1]['4. close'])
print(yesterday_data)
print(day_before_yesterday_data)

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.

difference = round(abs(yesterday_data - day_before_yesterday_data), 2)
print (difference)

# Find the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_difference = round((difference / yesterday_data * 100), 2)
print(f"{percentage_difference}%")

# If percentage difference is greater than 5, use the News API to get articles related to the COMPANY_NAME.
news_response = requests.get(url = NEWS_ENDPOINT, params = NEWS_PARAMS)

# Use Python slice operator to create a list that contains the first 3 articles.
news_list = news_response.json()['articles'][:3]
# print(news_list)

# Create a new list of the first 3 article's headline and description using list comprehension.
formatted_article = [f"Headline: {article['title']}\n\nBrief: {article['description']}" for article in news_list]
# print(formatted_article)
# Send each article as a separate message via Twilio.

client = Client(TWILIO_APP_ID, TWILIO_API_KEY)
# Adjust percentage value for sms alert as you see fit

if percentage_difference > 10:
    print("get news")

    for article in formatted_article:
        message = client.messages.create(
                            body=article,
                            from_='your sender number',
                            to='your receiver number'
                        )
        print(message.sid)

# Optional: Format the message like this:

"""
TSLA: 🔺2%
Headline:  
Brief: 
or
"TSLA: 🔻5%
Headline:  
Brief: 
"""