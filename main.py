import discord
import os

import config
import crypto
import stock
import util
from keep_alive import keep_alive


# ----------------------------------------------------------------------------------
# Get output message 
# Input: msg_data retrieved from users discord message; `$moon msg_data`
# Output: full discord message
# ----------------------------------------------------------------------------------
def get_price_message(msg_data):
  price_message = crypto.get_price(msg_data)

  if not price_message:
    price_message = stock.get_price(msg_data)

  if not price_message:
    price_message = '{0} is not supported!'.format(msg_data)
  
  return price_message


client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  if msg.startswith(config.MSG_PREFIX):
    msg_data = msg[len(config.MSG_PREFIX):].lstrip()
    if not util.is_msg_data_valid(msg_data):
      return

    if (msg_data == 'trending'):
      crypto_trending = crypto.get_trending()
      stock_trending = stock.get_trending()
      output_message = stock_trending + crypto_trending
    else:
      output_message = get_price_message(msg_data)
    
    await message.channel.send(output_message)

keep_alive()
client.run(os.environ['BOT_TOKEN'])

