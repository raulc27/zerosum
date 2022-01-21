from flask import Flask, request,jsonify

api = Flask(__name__)


@app.route('/shows')
def list():
    result = show.ShowModel.list_shows()
    return {'showlist':result},200

@app.route('/show/<int:int>/update', methods=['PUT'])
def update_show(id):
    request_data = request.get_json()
    result = show.ShowModel.find_by_id(id)
    if result:
        result.name = request_data['name']
        result.update()
        return {'message':'Série atualizada com sucesso'}, 200
    else:
        return {'message':'Série não encontrada'}, 404

if __name__ == '__main__':
    api.run(port=5000, debug=True)