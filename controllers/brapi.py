from flask import jsonify
from brapi import AsyncBrapi
from dotenv import load_dotenv
import os
import asyncio
import requests
import json

load_dotenv()
BRAPI_TOKEN = os.getenv("BRAPI_TOKEN");
BASE_URL = "https://brapi.dev/api/quote/";

params = {
    "range": "5d",
    "interval": "1d",
    "fundamental": "true",
    "dividends": "true",
    "modules": [
        "summaryProfile",
        "balanceSheetHistory",
        "financialData"
    ]
}

class Brapi:
    @staticmethod
    def get_stock_data(ticker):
        url = f"{BASE_URL}{ticker}"
        headers = {
            "Authorization": f"Bearer {BRAPI_TOKEN}"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch data from Brapi"}), response.status_code

    
    @staticmethod
    def get_async_stock_data(ticker):
        async_brapi = AsyncBrapi(api_key=BRAPI_TOKEN)
        # data = async_brapi.get_quote(
        #     ticker, 
        #     range="5d", 
        #     interval="1d", 
        #     fundamental=True, 
        #     dividends=True, 
        #     modules=["summaryProfile", 
        #     "balanceSheetHistory", 
        #     "financialData"])
        data = async_brapi.quote.retrieve(tickers=ticker)
        return jsonify(data)


    
        