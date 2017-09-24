import os
from flask import Flask, jsonify, abort, make_response, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config.from_pyfile('config.py')
APP_CONFIG = app.config['APP_CONFIG']

# mysql config
app.config['MYSQL_HOST'] = APP_CONFIG['mysql_host']
app.config['MYSQL_USER'] = APP_CONFIG['mysql_user']
app.config['MYSQL_PASSWORD'] = APP_CONFIG['mysql_password']
app.config['MYSQL_DB'] = APP_CONFIG['mysql_db']
app.config['MYSQL_CURSORCLASS'] = APP_CONFIG['mysql_cursorclass']

mysql = MySQL(app)

@app.route('/')
@cross_origin(supports_credentials=True)
def home():
    return jsonify({'message' : "hello kadek, it's working!"}), 200

@app.route('/ps4-games/api/v1/list', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_tasks():
    page = request.args.get('page', 0)
    perpage = 5;
    startat = int(page)*perpage
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM ps4_games limit %s, %s", [startat, perpage])
    result_set = cur.fetchall()
    cur.close()

    data = [{
        'page': page,
        'total_records': len(result_set),
        'data': result_set
    }]

    if result > 0:
        return jsonify(data), 200
    else:
        msg = 'no ps4 game found'
        return jsonify({'message': msg}), 200

@app.route('/ps4-games/api/v1/detail/<int:id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_task(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM ps4_games WHERE id = %s", [id])
    result_set = cur.fetchone()
    cur.close()

    if result_set > 0:
        return jsonify(result_set), 200
    else:
        msg = 'no ps4 game found'
        return jsonify({'message': msg}), 200

@app.route('/ps4-games/api/v1/create', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_task():
    if not request.json or not 'title' in request.json:
        abort(404)
    if not 'release_date' in request.json:
        return jsonify('release_date not found in the json'), 201

    title = request.json['title']
    genre = request.json.get('genre', "")
    exclusive = request.json.get('exclusive', "no")
    developer = request.json.get('developer', "")
    publisher = request.json.get('publisher', "")
    image_link = request.json.get('image_link', "")
    release_date = request.json.get('release_date')
    created_by = 1

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO ps4_games (title, genre, exclusive, developer, publisher, image_link, release_date, created_by) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", [title, genre, exclusive, developer, publisher, image_link, release_date, created_by])
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'success'}), 201

@app.route('/ps4-games/api/v1/update/<int:id>', methods=['PUT'])
@cross_origin(supports_credentials=True)
def update_task(id):
    if not request.json or not 'title' in request.json:
        abort(404)

    title = request.json['title']
    genre = request.json.get('genre', "")
    exclusive = request.json.get('exclusive', "no")
    developer = request.json.get('developer', "")
    publisher = request.json.get('publisher', "")
    image_link = request.json.get('image_link', "")
    release_date = request.json.get('release_date')

    cur = mysql.connection.cursor()
    app.logger.info(title)
    cur.execute ("UPDATE ps4_games SET title=%s, genre=%s, exclusive=%s, developer=%s, publisher=%s, image_link=%s WHERE id=%s", (title, genre, exclusive, developer, publisher, image_link, id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message':'success'}), 200

@app.route('/ps4-games/api/v1/delete/<int:id>', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ps4_games WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'success'}), 200

@app.errorhandler(404)
@cross_origin(supports_credentials=True)
def not_found(error):
    return make_response(jsonify({'message': 'Not found'}), 404)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=APP_CONFIG['app_debug_mode'])