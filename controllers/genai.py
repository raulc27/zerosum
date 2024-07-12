import os
import marko
from flask import jsonify
import yfinance as yf
import google.generativeai as genai
from datetime import date, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots



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
        timeprices = yf.download(cls, start=lastweek, end=today)
        quote = yf.Ticker(cls)
        priceresume = timeprices.head(-1)
        
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Candlestick(name=f'Variação da cotação de {cls}', 
                                    x=timeprices.index, 
                                    open=timeprices['Open'],
                                    high=timeprices['High'],
                                    low=timeprices['Low'],
                                    close=timeprices['Close'],
                                    showlegend=True),
                                    row=1,
                                    col=1)
        fig.update_yaxes(title_text="<b>Preço {cls} (R$)", row=1, col=1)
        fig.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500)
        graph = fig.show()

        image = [
            {
                "mime_type": "image/png",
                "content": graph
            }            
        ]

        
        _prompt = f"""You are an economist with market knowledge,
        make a resume about {cls}, show its {priceresume} and comment about it (the prices diferences, did the prices fall ?
        are they in an uptrend or downtrend, from {today} to {lastweek} ?),
        show {quote.quarterly_financials.to_html()} and comment about the diferences between dates, convert the prices to money format,
        in brazilian portuguese, show {image} as image at the begining of the resume
        """
    
        response = model.generate_content(_prompt)
        return jsonify({
            "response": marko.convert(response.text)
        })