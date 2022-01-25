import pandas as pd
import yfinance as yf

class ShowMarket:

    def result_show():
     timeprices = yf.download("BOVA11.SA SPY")
     return timeprices.head(-1)
