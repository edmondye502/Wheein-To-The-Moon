import discord
import os
import requests
from keep_alive import keep_alive

TRENDING_CAP = 5
CRYPTO_URL = 'https://api.coingecko.com/api/v3/'
MARKET_URL = 'https://yfapi.net/'

client = discord.Client()

# ----------------------------------------------------------------------------------
# Get the price of a cryptocurrency
# Input: crypto symbol, id, or name
# Output: full discord message with price or False
# ----------------------------------------------------------------------------------
def get_crypto_price(crypto):
  response = requests.get(CRYPTO_URL + 'coins/markets?vs_currency=usd')
  data = response.json()
  
  for i in range(len(data)):
    if data[i]['id'] == crypto.lower() or data[i]['symbol'] == crypto.lower() or data[i]['name'] == crypto.title():
      price = data[i]['current_price']
      return get_output_string(data[i]['name'], price, data[i]['price_change_percentage_24h'])
  return False

def get_yf_data(ticker):
  url = MARKET_URL + 'v6/finance/quote'
  querystring = {"symbols": ticker}
  headers = {
    'x-api-key': os.environ['YAHOO_KEY']
  }
  response = requests.request("GET", url, headers=headers, params=querystring)
  data = response.json()['quoteResponse']['result']
  return data

# ----------------------------------------------------------------------------------
# Get the price of a stock
# Input: ticker symbol (company name is not supported)
# Output: full discord message with price or False
# ----------------------------------------------------------------------------------
def get_ticker_price(ticker):
  data = get_yf_data(ticker)
  if data:
    if data[0]['quoteType'] == 'MUTUALFUND':
      return False
    
    if 'displayName' in data[0]:
      displayName = data[0]['displayName']
    elif 'longName' in data[0]:
      displayName = data[0]['longName']
    elif 'shortName' in data[0]:
      displayName = data[0]['shortName']
    else:
      displayName = data[0]['symbol']
    return get_output_string(displayName, data[0]['regularMarketPrice'], data[0]['regularMarketChangePercent'])
  return False

# ----------------------------------------------------------------------------------
# Get output message 
# Input: msg_data retrieved from users discord message; `$moon msg_data`
# Output: full discord message
# ----------------------------------------------------------------------------------
def get_price_message(msg_data):
  price_message = get_crypto_price(msg_data)

  if not price_message:
    price_message = get_ticker_price(msg_data)

  if not price_message:
    price_message = '{0} is not supported!'.format(msg_data)
  
  return price_message

# ----------------------------------------------------------------------------------
# Get the full output message
# Input: name, price, and 24hr to be shown in the message
# Output: string output message
# ----------------------------------------------------------------------------------
def get_output_string(displayName, price, change):
  return 'The current price of {0} is {1}'.format(displayName, get_price_string(price, change))

def get_price_string(price, change):
  if change >= 0:
    chartSymbol = ':chart_with_upwards_trend:'
  else:
    chartSymbol = ':chart_with_downwards_trend:'
  return '${0} ({1}% {2})'.format(price, change, chartSymbol)

# ----------------------------------------------------------------------------------
# Get trending crypto and stocks 
# Input: None
# Output: full discord message with top 5 trending crypto/stock
# ----------------------------------------------------------------------------------
def get_trending():
  trending = {}
  response = requests.get(CRYPTO_URL + 'search/trending')
  data = response.json()['coins']

  trending_crypto = []
  if data:
    for i in range(TRENDING_CAP):
      cryptoSymbol = data[i]['item']['symbol']
      cryptoID = data[i]['item']['id']
      response = requests.get(CRYPTO_URL + 'coins/' + cryptoID)
      cryptoData = response.json()['market_data']
      trending_crypto.append([cryptoSymbol, cryptoData['current_price']['usd'], cryptoData['price_change_percentage_24h']])
    trending['crypto'] = trending_crypto

  url = MARKET_URL + 'v1/finance/trending/US'
  headers = {
    'x-api-key': os.environ['YAHOO_KEY']
  }
  response = requests.request("GET", url, headers=headers)
  data = response.json()['finance']['result'][0]
  
  trending_market = []
  if data:
    for i in range(TRENDING_CAP):
      marketSymbol = data['quotes'][i]['symbol']
      marketData = get_yf_data(marketSymbol)[0]
      trending_market.append([marketSymbol, marketData['regularMarketPrice'], marketData['regularMarketChangePercent']])
    trending['market'] = trending_market

  output_message = ''

  if (trending['crypto']):
    output_message += "The top 5 trending cryptocurrencies right now are: \n"
    output_message += ''.join("\t" + str(i+1) + ') ' + str(e[0]) + ': '+ get_price_string(e[1], e[2]) + "\n" for i, e in enumerate(trending['crypto']))
  
  if (trending['market']):
    output_message += "\nThe top 5 trending stocks right now are: \n"
    output_message += ''.join("\t" + str(i+1) + ') ' + str(e[0]) + ': '+ get_price_string(e[1], e[2]) + "\n" for i, e in enumerate(trending['market']))
  
  return 'Could not get any trending data. Try again later!' if not trending else output_message


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  if msg.startswith('$moon'):
    msg_data = msg[len('$moon'):].lstrip()
    if msg_data.isdigit():
      return

    if (msg_data == 'trending'):
      output_message = get_trending()
    else:
      output_message = get_price_message(msg_data)
    
    await message.channel.send(output_message)

keep_alive()
client.run(os.environ['BOT_TOKEN'])

