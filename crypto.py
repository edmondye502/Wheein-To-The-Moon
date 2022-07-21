import config
import requests
import util

# ----------------------------------------------------------------------------------
# Get the price of a cryptocurrency
# Input: crypto symbol, id, or name
# Output: output msg or False
# ----------------------------------------------------------------------------------
def get_price(crypto):
  response = requests.get(config.CRYPTO_URL + 'coins/markets?vs_currency=usd')
  data = response.json()

  for i in range(len(data)):
    if data[i]['id'] == crypto.lower() or data[i]['symbol'] == crypto.lower() or data[i]['name'] == crypto.title():
      price = data[i]['current_price']
      return util.get_output_string(data[i]['name'], price, data[i]['price_change_percentage_24h'], 0, 0)

  return False

def get_specific_price(crypto):
  response = requests.get(config.CRYPTO_URL + 'coins/' + crypto.lower())
  data = response.json()
  if data and 'error' not in data:
    return util.get_output_string(data['name'], data['market_data']['current_price']['usd'], data['market_data']['price_change_percentage_24h'], 0, 0)
  return False

# ----------------------------------------------------------------------------------
# Get trending crypto
# Input: None
# Output: output msg
# ----------------------------------------------------------------------------------
def get_trending():
  response = requests.get(config.CRYPTO_URL + 'search/trending')
  data = response.json()['coins']

  trending_crypto = []
  if data:
    for i in range(config.TRENDING_CAP):
      cryptoSymbol = data[i]['item']['symbol']
      cryptoID = data[i]['item']['id']
      response = requests.get(config.CRYPTO_URL + 'coins/' + cryptoID)
      cryptoData = response.json()['market_data']
      trending_crypto.append([cryptoSymbol, cryptoData['current_price']['usd'], cryptoData['price_change_percentage_24h']])

  output_message = ''
  if (trending_crypto):
    output_message += "\nThe top 5 trending cryptos right now are: \n"
    output_message += ''.join("\t" + str(i+1) + ') ' + str(e[0]) + ': '+ util.get_price_string(e[1], e[2]) + "\n" for i, e in enumerate(trending_crypto))
  
  return 'Could not get any trending crypto data. Try again later!' if not trending_crypto else output_message
