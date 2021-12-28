# ----------------------------------------------------------------------------------
# Validate if a message should be processed
# Input: msg data
# Output: boolean
# ----------------------------------------------------------------------------------
def is_msg_data_valid(msg_data):
  if msg_data.isdigit():
    return False

  return True

# ----------------------------------------------------------------------------------
# Get the full output message to be displayed on discord
# Input: name, price, and change to be shown in the message
# Output: string output message
# ----------------------------------------------------------------------------------
def get_output_string(displayName, price, change):
  return 'The current price of {0} is {1}'.format(displayName, get_price_string(price, change))

# ----------------------------------------------------------------------------------
# Get price string $xx.xx (x% chart_emoji)
# Input: price and change to be shown in the message
# Output: string output message
# ----------------------------------------------------------------------------------
def get_price_string(price, change):
  if change >= 0:
    chartSymbol = ':chart_with_upwards_trend:'
  else:
    chartSymbol = ':chart_with_downwards_trend:'
  return '${0} ({1}% {2})'.format(format_price(price), format_percent(change), chartSymbol)

def format_price(price):
  if price >= 1:
 	  return '{:,.2f}'.format(price)
  else:
    num = '{:.4g}'.format(price)
    if 'e-' in num:
      a, b = num.split('e-')
      a = a.replace('.', '')
      b = int(b)
      return '0.' + '0' * (b - 1) + a
    else:
      return num

def format_percent(change):
  return '{:,.3f}'.format(change)

def get_symbol_lists(msg_data):
  return msg_data.split('/')
