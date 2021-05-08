from binance.client import Client

from API_CONFIG import config

sym = 'ethusdt'
intval = '1m'
rsi_period = 14
rsi_overbought = 70
rsi_oversold = 30

# define websockets connections
socket = "wss://stream.binance.com:9443/ws/" + sym + "@kline_" + intval

# define api client
client = Client(config.api_key, config.api_secret)


def account_balance():
  status = client.get_account_api_trading_status()
  balance = str(client.get_asset_balance(asset='CAD'))
  return status, balance


print(account_balance()[0])


def quantity_to_buy(balance, close, percent_of_balance=5):
  if balance is None:
    return ("balance is equal to None, check account balance, and check asset settings")
  else:
    balance = float(balance)
    price_per = float(close)
    percent_of_balance = float(percent_of_balance) / 100
    quantity = price_per / balance * percent_of_balance
    return quantity


quantity = quantity_to_buy(balance=None, close=1000, percent_of_balance=10)

print(quantity)
