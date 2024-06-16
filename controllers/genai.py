import os
import marko
from flask import jsonify
import yfinance as yf
import google.generativeai as genai
from datetime import date, timedelta



class Genai:
    
    today = date.today()
    lastweek = today - timedelta(days=7)

    genai.configure(api_key=os.getenv("GENAI_API_KEY"))

    config = {
    'temperature': 0,
    'top_k': 20,
    'top_p': 0.9,
    'max_output_tokens': 500
    }
    
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                            generation_config=config,
                            safety_settings=safety_settings)

    def market_resume(today=today, lastweek=lastweek, model=model):
        #timeprices = yf.download("BOVA11.SA SPY")
        _prompt = f"""Make a resume in brazilian portuguese, using three paragraphs, 
        from {lastweek} until {today}, about brazilian financial market and main news related, show links to the sources."""
    
        response = model.generate_content(_prompt)
        return jsonify({
            "response": marko.convert(response.text)
        })
        

    def ticker_resume(cls, today=today, lastweek=lastweek, model=model):
        #timeprices = yf.download("BOVA11.SA SPY")
        _prompt = f"Make a resume about {cls} related news in brazilian portuguese, using three paragraphs, from {lastweek} until {today}, show links to the sources"
    
        response = model.generate_content(_prompt)
        return jsonify({
            "response": marko.convert(response.text)
        })