import os
import marko
from flask import jsonify
from brapi import Brapi
import google.generativeai as genai
from google.generativeai import types
from datetime import date, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
import urllib, base64



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

    model = genai.GenerativeModel(model_name="gemini-2.5-pro",
                            generation_config=config,
                            #safety_settings=safety_settings
                            )
    
    def create_candlestick_chart(timeprices, cls):
        """Creates a candlestick chart and returns it as a base64-encoded string.

        Args:
            timeprices: Brapi.get_async_stock_data.download... with price time series data.
            cls (str): Class name or identifier for the chart.

        Returns:
            str: Base64-encoded image data of the candlestick chart.
        """

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


        # fig = go.candlestick(
        #     timeprices,
        #     x=timeprices.index,
        #     open="Open",
        #     high="High",
        #     low="Low",
        #     close="Close",
        #     title=f'Variação da cotação de {cls}',
        #     showlegend=True
        # )

        fig.update_layout(
            yaxis_title=f'<b>Preço {cls} (R$)</b>',
            xaxis_rangeslider_visible=False,
            width=1000,
            height=500
        )

        # Capture image data and encode as base64
        img_data = io.BytesIO()
        fig.write_image(img_data, format="png")
        img_data.seek(0)  # Rewind to beginning
        base64_encoded_img = base64.b64encode(img_data.read()).decode("utf-8")

        # Construct the URI
        uri = f'data:image/png;base64,{urllib.parse.quote(base64_encoded_img)}'

        return uri

    def market_resume(today=today, lastweek=lastweek, model=model):
        #timeprices = Brapi.get_async_stock_data.download("BOVA11.SA SPY")
        _prompt = f"""You are an economist with brazilian market knowledge, make a resume in brazilian portuguese, using at least three paragraphs, 
        from {lastweek} until {today}, explaining about the brazilian financial market and main news related, make the resume in brazilian portuguese.
        """
    
        response = model.generate_content(_prompt)
        return jsonify({
            "response": marko.convert(response)
        })
        

    def ticker_resume(cls, today=today, lastweek=lastweek, model=model):
        timeprices = Brapi.get_async_stock_data(cls, start=lastweek, end=today)
        quote = Brapi.get_async_stock_data(cls)
        priceresume = timeprices.head(-1)
        
        htmlGraph = Genai.create_candlestick_chart(timeprices, cls)
                
        _prompt = f"""You are an economist with brazilian market knowledge,
        make a resume about {cls}, show its {priceresume} in a table and comment about that prices (in money format, how did the prices perform ?
        are they in an uptrend or downtrend, from {today} to {lastweek} ?),
        show {quote.quarterly_financials.to_html()} in a table and comment about the timeseries, convert the prices to money format,
        make the resume in brazilian portuguese.
        """
    
        response = model.generate_content(
            _prompt
            )
        return jsonify({
            "response": marko.convert(response.text),
            "graph": htmlGraph
        })