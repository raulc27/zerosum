from flask import Flask, request, jsonify, Response, g, render_template
from flask_cors import CORS, cross_origin
from controllers import mainprices, genai, brapi

api = Flask(__name__)
cors=CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

@api.route('/')
@cross_origin()
def get_generic():
    return {
        '/ticker/fundamentals/TICKER.sa':'Fundamentals (quarterly)',
        '/ticker/cashflow/TICKER.sa':'Cashflow (quarterly)',
        '/ticker/TICKER.sa':'Basic info about TICKSER.sa',
        '/genai/resume_market':'Resume market',
        '/genai/resume_ticker/TICKER.sa':'Basic info about TICKSER.sa',
    }, 200

@api.route('/ticker/<string:name>')
@cross_origin()
def get_show(name):
    result = mainprices.ShowMarket.show_ticker(name)
    if result:
        return result, 200
    return {'message':'not found'}, 404

@api.route('/ticker/fundamentals/<string:name>')
@cross_origin()
def get_fundamentals_show(name):
    result = mainprices.ShowMarket.fundamentals_ticker(name)
    if result:
        return result, 200
    return {'message':'not found'}, 404

@api.route('/ticker/cashflow/<string:name>')
@cross_origin()
def get_cashflow_show(name):
    result = mainprices.ShowMarket.cashflow_ticker(name)
    if result:
        return result, 200
    return {'message':'not found'}, 404


@api.route('/genai/resume_market')
@cross_origin()
def market_resume_show():
    result = genai.Genai.market_resume()
    if result:
        return result, 200
    return {'message':'not found'}, 404

@api.route('/genai/resume_ticker/<string:name>')
@cross_origin()
def ticket_resume_show(name):
    result = genai.Genai.ticker_resume(name)
    if result:
        return result, 200
    return {'message':'not found'}, 404

@api.route('/brapi/quote/<string:name>')
@cross_origin()
def brapi_quote_show(name):
    result = brapi.Brapi.get_quote(name)
    if result:
        return result, 200
    return {'message':'not found'}, 404

if __name__ == '__main__':
    api.run(port=5000, debug=True)