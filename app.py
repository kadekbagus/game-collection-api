import os
from flask import Flask, jsonify, abort, make_response, request
from flask_mysqldb import MySQL

app = Flask(__name__)

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
def home():
    return jsonify({'message' : "hello kadek, it's working!"}), 200

@app.route('/ps4-games/api/v1/list', methods=['GET'])
def get_tasks():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM ps4_games")
    result_set = cur.fetchall()
    cur.close()

    if result > 0:
        return jsonify(result_set), 200
    else:
        msg = 'no ps4 game found'
        return jsonify({'message': msg}), 200

@app.route('/ps4-games/api/v1/detail/<int:id>', methods=['GET'])
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
def create_task():
    if not request.json or not 'title' in request.json:
        abort(404)
    if not 'release_date' in request.json:
        return jsonify('release_date not found in the json'), 201

    title = request.json['title']
    genre = request.json.get('genre', "")
    exclusive = request.json.get('exclusive', "")
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
def update_task(id):
    if not request.json or not 'title' in request.json:
        abort(404)

    title = request.json['title']
    genre = request.json.get('genre', "")
    exclusive = request.json.get('exclusive', "")
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
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ps4_games WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'success'}), 200

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': 'Not found'}), 404)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=APP_CONFIG['app_debug_mode'])