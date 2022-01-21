from flask import Flask, request,jsonify
from controllers import exchanges, tickers

api = Flask(__name__)


@app.route('/exchangeresult')
def list():
    result = exchanges.ShowExchanges.result_show()
    return {'exchanges_result':result},200


@app.route('/ticker/<string:name>')
def get_show(name):
    result = tickers.ShowTicker.find_by_name(name)
    if result:
        return result.json()
    return {'message':'not found'}, 404

if __name__ == '__main__':
    api.run(port=5000, debug=True)