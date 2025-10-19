from flask import jsonify
import os
import requests
import json

BRAPI_TOKEN = os.getenv("BRAPI_TOKEN");
BASE_URL = "https://brapi.dev/api/quote/";
params={?token=&range=5d&interval=1d&fundamental=true&dividends=true&modules=summaryProfile,balanceSheetHistory,financialData}

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
  

    
        