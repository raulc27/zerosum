import os
import marko
from flask import jsonify
import yfinance as yf
import google.generativeai as genai
from datetime import date, timedelta



class Genai:

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

    def market_resume(model=model):
        #timeprices = yf.download("BOVA11.SA SPY")
        _prompt = """Make a resume in brazilian portuguese, using three paragraphs, 
        from yesterday until now, about brazilian financial market, range B3 exchange indexes
        points [Indice Bovespa, Indice Brasil 100 (IBrX 100), Indice Brasil 50 (IBrX 50), Indice Brasil Amplo (IBrA B3)]
        and main news related."""
    
        response = model.generate_content(_prompt)
        return jsonify({
            "response": marko.convert(response.text)
        })
        

    def ticket_resume(cls, model=model):
        #timeprices = yf.download("BOVA11.SA SPY")
        _prompt = f"Make a resume about {cls} and its prices in brazilian portugues, using three paragraphs, from the last week until now, and main news related"
    
        response = model.generate_content(_prompt)
        return jsonify({
            "response": marko.convert(response.text)
        })