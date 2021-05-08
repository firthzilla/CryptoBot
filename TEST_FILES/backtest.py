import datetime
import backtrader as bt
from Strategies.strategies import RSIStrategy

if __name__ == "__main__":
  cerebro = bt.Cerebro()
  cerebro.broker.setcash(5000.0)


  #add data to cerebro
  data = bt.feeds.YahooFinanceCSVData(
    dataname='CSV_FILES/ticker_ETH-USD.csv',
    # Do not pass values before this date
    fromdate=datetime.datetime(2020, 5, 9),
    # Do not pass values after this date
    todate=datetime.datetime(2021, 5, 8),
    reverse=False)


  cerebro.adddata(data)

  cerebro.addstrategy(RSIStrategy)


  print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

  cerebro.run()

  print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

  cerebro.plot()
