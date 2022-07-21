import os
import config
import requests
import util

# ----------------------------------------------------------------------------------
# Request trending stocks data from yahoo finance api
# Input: None
# Output: response data from yahoo finance
# ----------------------------------------------------------------------------------
def request_yf_trending_data():
  url = config.MARKET_URL + 'v1/finance/trending/US'
  headers = {
    'x-api-key': os.environ['YAHOO_KEY']
  }
  response = requests.request("GET", url, headers=headers)
  data = response.json()['finance']['result'][0]
  return data
# ----------------------------------------------------------------------------------
# Get data of a stock from yahoo finance api
# Input: stock ticker symbol
# Output: response data from yahoo finance
# ----------------------------------------------------------------------------------
def request_yf_stock_data(ticker):
  url = config.MARKET_URL + 'v6/finance/quote'
  querystring = {"symbols": ticker}
  headers = {
    'x-api-key': os.environ['YAHOO_KEY']
  }
  response = requests.request("GET", url, headers=headers, params=querystring)
  data = response.json()['quoteResponse']['result']
  return data

# ----------------------------------------------------------------------------------
# Get trending stocks 
# Input: None
# Output: output msg
# ----------------------------------------------------------------------------------
def get_trending():
  data = request_yf_trending_data()
  
  trending_stock = []
  if data:
    for i in range(config.TRENDING_CAP):
      marketSymbol = data['quotes'][i]['symbol']
      marketData = request_yf_stock_data(marketSymbol)[0]
      trending_stock.append([marketSymbol, marketData['regularMarketPrice'], marketData['regularMarketChangePercent']])

  output_message = ''
  if (trending_stock):
    output_message += "\nThe top 5 trending stocks right now are: \n"
    output_message += ''.join("\t" + str(i+1) + ') ' + str(e[0]) + ': '+ util.get_price_string(e[1], e[2]) + "\n" for i, e in enumerate(trending_stock))
  
  return 'Could not get any trending stock data. Try again later!' if not trending_stock else output_message


# ----------------------------------------------------------------------------------
# Get the price of a stock
# Input: ticker symbol (company name is not supported)
# Output: full discord message with price or False
# ----------------------------------------------------------------------------------
def get_price(ticker):
  data = request_yf_stock_data(ticker)
  if data:
    if data[0]['quoteType'] == 'MUTUALFUND':
      return False
    if 'regularMarketPrice' not in data[0]:
      return False

    if 'displayName' in data[0]:
      displayName = data[0]['displayName']
    elif 'longName' in data[0]:
      displayName = data[0]['longName']
    elif 'shortName' in data[0]:
      displayName = data[0]['shortName']
    else:
      displayName = data[0]['symbol']

    if 'postMarketPrice' in data[0]:
      postMarketPrice = data[0]['postMarketPrice']
      postMarketChange = data[0]['postMarketChange']
    else:
      postMarketPrice = 0
      postMarketChange = 0
    
    return util.get_output_string(displayName, data[0]['regularMarketPrice'], data[0]['regularMarketChangePercent'], postMarketPrice, postMarketChange)
  return False
  