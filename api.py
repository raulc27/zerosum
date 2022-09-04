from flask import Flask, request, jsonify
from controllers import mainprices

api = Flask(__name__)

@api.route('/')
def get_generic():
    return {
        '/ticker/fundamentals/TICKER.sa':'Fundamentals (quarterly)',
        '/ticker/cashflow/TICKER.sa':'Cashflow (quarterly)',
        '/ticker/TICKER.sa':'Basic info about TICKSER.sa',
    }, 200

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
        return result, 200
    return {'message':'not found'}, 404

@api.route('/ticker/cashflow/<string:name>')
def get_cashflow_show(name):
    result = mainprices.ShowMarket.cashflow_ticker(name)
    if result:
        return result, 200
    return {'message':'not found'}, 404

if __name__ == '__main__':
    api.run(port=5000, debug=True)