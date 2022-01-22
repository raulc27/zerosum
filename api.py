from flask import Flask, request,jsonify
from controllers import mainprices, tickers

api = Flask(__name__)


@api.route('/exchangeresult')
def list():
    result = mainprices.ShowExchanges.result_show()
    return {'exchanges_result':result},200


@api.route('/ticker/<string:name>')
def get_show(name):
    result = tickers.ShowTicker.find_by_name(name)
    if result:
        return result.json()
    return {'message':'not found'}, 404

if __name__ == '__main__':
    api.run(port=5000, debug=True)