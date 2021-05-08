import yfinance as yf


symbol = ['ETH-USD']

def get_csv(symbol):
  tickerStrings = symbol
  for ticker in tickerStrings:
    data = yf.download(ticker, group_by="Ticker", period='365d', interval='1d')
    data['ticker'] = ticker  # add this column becasue the dataframe doesn't contain a column with the ticker
    data.to_csv(f'ticker_{ticker}.csv')  # ticker_AAPL.csv for example

get_csv(symbol=symbol)

