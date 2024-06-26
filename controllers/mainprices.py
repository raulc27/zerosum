import pandas as pd
import yfinance as yf
from flask import jsonify
import json

class ShowMarket:

    def result_show():
     timeprices = yf.download("BOVA11.SA SPY")
     return timeprices.head(-1)

    def show_ticker(cls):
        quote = yf.Ticker(cls)
        return quote.info
    """  
    return {
        "Name": quote.info['shortName'],
        "Symbol": quote.info['symbol'],
        "Price": quote.info['currentPrice'],
        "Profit": quote.info['profitMargins'],
        "Volume": quote.info['volume'],
        "AverageVolume": quote.info['averageVolume'],
        "MarketCap": quote.info['marketCap'],
        } 
    """
        

    def fundamentals_ticker(cls):
        quote = yf.Ticker(cls)
        return quote.quarterly_financials.to_json()

    def cashflow_ticker(cls):
        quote = yf.Ticker(cls)
        return quote.quarterly_cashflow.to_json()

    def quote(cls):
        price = yf.download(cls)
        return price.info