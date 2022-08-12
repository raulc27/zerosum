from flask import Flask, request,jsonify
from controllers import mainprices

api = Flask(__name__)


@api.route('/exchangeresult/')
def list():
    result = mainprices.ShowMarket.result_show()
    if result:
        return result.json(), 200
    return {'Error':'no results'},404

@api.route('/ticker/<string:name>')
def get_show(name):
    result = mainprices.ShowMarket.show_ticker(name)
    if result:
        return result, 200
    return {'message':'not found'}, 404

@api.route('/ticker/fundamentals/<string:name>')
def get_fundamentals_show(name):
    result = mainprices.ShowMarket.fundamentals_ticker(name)
    if result:
        return result.json(), 200
    return {'message':'not found'}, 404

@api.route('/quote/<string:symbol>')
def display_quote(symbol):
 #   symbol = request.args.get('symbol', default="AAPL")
    result = mainprices.ShowMarket.ticker(symbol)
    if result:
        return result.json(), 200
    return {"Error":"Could not retrieve info"}, 404

if __name__ == '__main__':
    api.run(port=5000, debug=True)