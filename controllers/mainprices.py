import pandas as pd
import yfinance as yf

class ShowMarket:

    def result_show():
     timeprices = yf.download("BOVA11.SA SPY")
     return timeprices.head(-1)

    def show_ticker(cls):
        price = yf.download(cls)
        return price.head(-1)
    
    def quote(cls):
        price = yf.download(cls)
        return price.info