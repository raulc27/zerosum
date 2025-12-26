from flask import Flask, request, jsonify, Response, g, render_template
from functools import wraps
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
from controllers import genai, brapi
from flask_caching import Cache

load_dotenv()
cors_origin = os.getenv('CORS_ORIGIN', '*')
api = Flask(__name__)
cors=CORS(api, resources={r"/*": {"origins": cors_origin}})
api.config['CORS_HEADERS'] = 'Content-Type'

# Cache Configuration
is_prod = os.getenv('FLASK_ENV') == 'production'
if is_prod:
    redis_user = os.getenv('REDIS_USER') or os.getenv('READIS_USER')
    redis_password = os.getenv('REDIS_PASSWORD')
    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('REDIS_PORT')

    if redis_user:
        redis_url = f"redis://{redis_user}:{redis_password}@{redis_host}:{redis_port}"
    else:
        redis_url = f"redis://:{redis_password}@{redis_host}:{redis_port}"

    cache_config = {
        'CACHE_TYPE': 'RedisCache',
        'CACHE_REDIS_URL': redis_url
    }
else:
    cache_config = {
        'CACHE_TYPE': 'NullCache'
    }

api.config.from_mapping(cache_config)
cache = Cache(api)

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = os.getenv('CLIENT_API_KEY')
        if not api_key:
             # If no API key is set in env, we might want to allow everything or block everything.
             # Usually block or warn. For now, let's assume if it's not set, we block for security.
             return jsonify({'message': 'Server misconfiguration: API_KEY not set'}), 500
        
        if request.headers.get('X-API-Key') == api_key:
            return f(*args, **kwargs)
        else:
            return jsonify({'message': 'Unauthorized'}), 401
    return decorated_function

@api.route('/')
@cross_origin()
@require_api_key
def get_generic():
    return {
        '/genai/resume_market': 'Resume market',
        '/genai/resume_ticker/TICKER': 'Resume for specific ticker',
        '/brapi/quote/TICKER': 'Get stock quote data',
        '/brapi/async_quote/TICKER': 'Get stock quote data (async)',
        '/brapi/sync_quote/TICKER': 'Get stock quote data with modules',
        '/brapi/sync_quote_list': 'Get list of predefined stocks',
        '/brapi/sync_quote_by_sector/SECTOR': 'Get stocks by sector (top 10 by volume)',
        '/brapi/sync_quote_list_sectors': 'Get available sectors list',
    }, 200


@api.route('/genai/resume_market')
@cross_origin()
@require_api_key
def market_resume_show():
    result = genai.Genai.market_resume()
    if result:
        return result, 200
    return {'message':'not found'}, 404

@api.route('/genai/resume_ticker/<string:name>')
@cross_origin()
@require_api_key
def ticket_resume_show(name):
    result = genai.Genai.ticker_resume(name)
    if result:
        return result, 200
    return {'message':'not found'}, 404

@api.route('/brapi/quote/<string:name>')
@cross_origin()
@require_api_key
@cache.cached(timeout=300)
def brapi_quote_show(name):
    result = brapi.Brapi.get_stock_data(name)
    if result:
        return result, 200
    return {'message':'not found'}, 404

@api.route('/brapi/async_quote/<string:name>')
@cross_origin()
@require_api_key
@cache.cached(timeout=300)
async def brapi_async_quote_show(name):
    result = await brapi.Brapi.get_async_stock_data(name)
    if result:
        return result, 200
    return {'message':'not found'}, 404

@api.route('/brapi/sync_quote/<string:name>')
@cross_origin()
@require_api_key
@cache.cached(timeout=300)
def brapi_sync_quote_show(name):
    result = brapi.Brapi.get_sync_stock_data(name)
    if result:
        return result, 200
    return {'message':'not found'}, 404

@api.route('/brapi/sync_quote_list')
@cross_origin()
@require_api_key
@cache.cached(timeout=300)
def brapi_sync_quote_list_show():
    result = brapi.Brapi.get_sync_stock_data_list()
    if result:
        return jsonify(result), 200
    return {'message':'not found'}, 404

@api.route('/brapi/sync_quote_by_sector/<string:sector>')
@cross_origin()
@require_api_key
@cache.cached(timeout=300)
def brapi_sync_quote_by_sector_show(sector):
    result = brapi.Brapi.get_sync_stock_data_list_by_sector(sector)
    if result:
        return jsonify(result), 200
    return {'message':'not found'}, 404


@api.route('/brapi/sync_quote_list_sectors')
@cross_origin()
@require_api_key
@cache.cached(timeout=300)
def brapi_sync_quote_list_sectors_show():
    result = brapi.Brapi.get_available_sectors_list()
    if result:
        return jsonify(result), 200
    return {'message':'not found'}, 404


if __name__ == '__main__':
    api.run(port=5000, debug=True)
