from flask import jsonify
from brapi import AsyncBrapi, Brapi
from dotenv import load_dotenv
import os
import asyncio
import requests
import json

load_dotenv()
BRAPI_TOKEN = os.getenv("BRAPI_TOKEN");
BASE_URL = "https://brapi.dev/api/quote/";
async_brapi = AsyncBrapi(api_key=BRAPI_TOKEN)
sync_brapi = Brapi(api_key=BRAPI_TOKEN)
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

TICKERS_LIST="PETR4,VALE3,CMIG4,MGLU3,BBAS3,B3SA3,BBDC4,ITUB4,WEGE3,EMBR3"

class Brapi:
    @staticmethod
    def get_stock_data(ticker):
        url = f"{BASE_URL}{ticker}?token={BRAPI_TOKEN}"
        headers = {
            "Authorization": f"Bearer {BRAPI_TOKEN}"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch data from Brapi"}), response.status_code

    
    @staticmethod
    async def get_async_stock_data(ticker):
        # async_brapi = AsyncBrapi(api_key=BRAPI_TOKEN)
        #data = await async_brapi.get_quote(
        #     ticker, 
        #     range="5d", 
        #     interval="1d", 
        #     fundamental=True, 
        #     dividends=True, 
        #     modules=["summaryProfile", 
        #     "balanceSheetHistory", 
        #     "financialData"])
        data = await async_brapi.quote.retrieve(tickers=ticker)
        #data = {}
        #print("data: ", data)
        if data.status_code == 200:
            return jsonify(data.json())
        else:
            return jsonify({"error": "Failed to fetch data from async Brapi"}), data.status_code


    @staticmethod
    def get_sync_stock_data(ticker):
        data = sync_brapi.quote.retrieve(tickers=ticker, modules="summaryProfile,balanceSheetHistory,defaultKeyStatistics,incomeStatementHistory")


        data_result = data.results[0]
        data_result_dict = data_result.dict()
        
        return data_result_dict 

    
    @staticmethod
    def get_sync_stock_data_list():
        data = sync_brapi.quote.retrieve(tickers=TICKERS_LIST)

        data_result = data.results
        data_result_dict = data_result.dict()
        
        return data_result_dict 
    
        
