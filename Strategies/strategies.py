import backtrader as bt



# Create a Stratey
class TestStrategy(bt.Strategy):

  def log(self, txt, dt=None):
    ''' Logging function for this strategy'''
    dt = dt or self.datas[0].datetime.date(0)
    print('%s, %s' % (dt.isoformat(), txt))

  def __init__(self):
    # Keep a reference to the "close" line in the data[0] dataseries
    self.dataclose = self.datas[0].close

  def next(self):
    # Simply log the closing price of the series from the reference
    self.log('Close, %.2f' % self.dataclose[0])



class RSIStrategy(bt.Strategy):
  def log(self, txt, dt=None):
    ''' Logging function for this strategy'''
    dt = dt or self.datas[0].datetime.date(0)
    print('%s, %s' % (dt.isoformat(), txt))

  def __init__(self):
    self.dataclose = self.datas[0].close
    self.rsi = bt.talib.RSI(self.data, period=14)
    self.ema26 = bt.talib.EMA(self.data, timeperiod=26)
    self.ema12 = bt.talib.EMA(self.data, timeperiod=12)
    # self.macd = self.ema12 - self.ema26

  def next(self):
    if self.ema12 > self.ema26 and not self.position:
      self.buy(size=1)
      self.log('Buy, %.2f' % self.dataclose[0])

    if self.ema26 > self.ema12 and self.position:
      self.close(size=1)
      self.log('Sell, %.2f' % self.dataclose[0])


