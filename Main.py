import json
import numpy
import talib
import websocket
from binance.client import Client
from binance.enums import *
from playsound import playsound
from API_CONFIG import config
#from Binanace_functions import order, account_balance, profit, quantity_to_buy
# define strategy variables that will be used to seek out and define entry and exit points
sym = 'ethusdt'
intval = '1m'
rsi_period = 14
rsi_overbought = 70
rsi_oversold = 30

# define websockets connections
socket = "wss://stream.binance.com:9443/ws/" + sym + "@kline_" + intval

# define api client
client = Client(config.api_key, config.api_secret)

# variables to hold price data on purchases and sell orders
initial_price = 0
final_price = 0

# define whether in position state or not
position = False
# variable to hold quanity amount
quantity_amount = 0

# create a array that holds data
closes = []
# fast over slow
macd_over_sig = False


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
  try:
    print("sending order")
    order = client.create_order(symbol=symbol, side=side, quantity=quantity)
    print(order)
  except Exception as e:
    print('an exception occurred -{}'.format(e))
    return False
  return True


# define a account balance lookup function
def account_balance():
  status = client.get_account_api_trading_status()
  balance = client.get_asset_balance(asset='CAD')
  return status, balance


# define a calculated buy quantity function based on account balance we want to
def quantity_to_buy(balance, close, percent_of_balance=5):
  if balance is None:
    return ("balance is equal to None, check account balance, and check asset settings")
  else:
    balance = float(balance)
    price_per = float(close)
    percent_of_balance = float(percent_of_balance) / 100
    quantity = price_per / balance * percent_of_balance
    return quantity


# define profit from transaction
def profit(initial=initial_price, final=final_price):
  profit = final - initial
  profit_percentage = profit / initial * 100
  return profit, profit_percentage


# MAIN CALLED FUNCTION
if __name__ == "__main__":
  def on_open(ws):
    print('Account Status information:')
    print(account_balance()[0])
    playsound('audio_clips/HorseRace.mp3')
    print("open connection")


  def on_close(ws):
    playsound('audio_clips/ManOutWindow.mp3')
    print("close connection")


  def on_message(ws, message):
    global position, macd_over_sig, rsi
    # JSON interpretation from message
    json_message = json.loads(message)
    # define candle state for strategy
    candle = json_message['k']
    # print(candle)
    is_closed = candle['x']
    # define closed candle
    if candle['x']:
      close = candle['c']
      closes.append(float(close))
      np_closes = numpy.array(closes, dtype=float)
      # print(np_closes[len(np_closes) - 1])
      close_EMA12 = talib.EMA(np_closes, timeperiod=12)
      close_EMA26 = talib.EMA(np_closes, timeperiod=26)
      close_macd = talib.MACD(np_closes, fastperiod=12, slowperiod=26, signalperiod=9)
      macd_line = close_macd[0]
      macd_signal = close_macd[1]
      macd_hist = close_macd[2]

      if len(closes) > rsi_period:
        rsi = talib.RSI(np_closes, rsi_period)
      # define if state represents a buy signal
      if macd_line[-1] > macd_signal[-1]:
        macd_over_sig = True
        print(np_closes[len(np_closes) - 1])
        print('macd_over_sig equals')
        print(macd_over_sig, macd_line[-1], macd_signal[-1])
        if rsi[-1] < 55:
          print('RSI under 55')
          print(rsi[-1])

          if position is False:
            # account balance lookup
            balance = account_balance()[-1]
            # quantity to buy lookup
            quantity = quantity_to_buy(balance=balance, close=np_closes[len(np_closes) - 1])
            # order = buy(quantity to buy)
            order = order(buy, quantity=quantity, symbol=sym)
            if order is True:
              print('position is false')
              # if position = False
              print('buy buy buy')
              # order(buy)
              position = True
              playsound('audio_clips/Triplebuy.mp3')
              print(np_closes[len(np_closes) - 1])
              print("position equals")
              print(position)
            else:
              print('order not fufilled')
        else:
          print(rsi[-1])
          print('order not made, RSI is over 55')
      else:
        macd_over_sig = False
        print(np_closes[len(np_closes) - 1])
        print('macd_over_sig equals')
        print(macd_over_sig, macd_line[-1], macd_signal[-1])

      # define if state represents a sell signal
      if rsi > 70:
        print('rsi over 70')
        if position is True:
          print('position is true')
          # if state represents a sell signal and in_position = True
          # using same quantity from buy order
          # order = sell(quantity amount)
          order = order(sell, quantity=quantity, symbol=sym)
          if order is True:
            print('Sell')
            position = False
            playsound('audio_clips/SELLSELLSELL.mp3')
            print(np_closes[len(np_closes) - 1])
            print("position equals")
            print(position)
          else:
            print('order not fufilled')
          # define profit from transaction = sell price - bought price
        else:
          print('RSI over 70 but you do not have anything to sell')


  ws = websocket.WebSocketApp(socket, on_open=on_open, on_close=on_close, on_message=on_message)

  ws.run_forever()
