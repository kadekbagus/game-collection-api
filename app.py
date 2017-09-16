import os
from flask import Flask, jsonify, abort, make_response, request, json
from flask_mysqldb import MySQL
from pprint import pprint

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    },
    {
        'id': 3,
        'title': u'Get Laid',
        'description': u'Find a beautiful girl and get laid',
        'done': False
    }
]

# mysql config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'lomax64'
app.config['MYSQL_DB'] = 'ps4_game_collection'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def home():
    return jsonify({'message' : "hello kadek, it's working!"}), 200

@app.route('/ps4-games/api/v1/list', methods=['GET'])
def get_tasks():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM ps4_games")
    result_set = cur.fetchall()

    if result_set > 0:
        return jsonify(result_set), 200
    else:
        msg = 'no ps4 game found'
        return jsonify(msg), 200

@app.route('/ps4-games/api/v1/detail/<int:id>', methods=['GET'])
def get_task(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM ps4_games WHERE id = %s", [id])
    result_set = cur.fetchone()
    
    if result_set > 0:
        return jsonify(result_set), 200
    else:
        msg = 'no ps4 game found'
        return jsonify(msg), 200


@app.route('/ps4-games/api/v1/create', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(404)
    if not 'release_date' in request.json:
        return jsonify('error'), 201

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
    return jsonify('success'), 201

@app.route('/ps4-games/api/v1/update/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/ps4-games/api/v1/delete/<int:id>', methods=['DELETE'])
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ps4_games WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    return jsonify({'success'}), 200

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)