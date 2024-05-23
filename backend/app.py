import requests
import json
import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

users_url = 'https://jsonplaceholder.typicode.com/users'
filename = 'database.json'
# filename = 'users.json'

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    # return "Hello from Flask!"
    return render_template('home.html')


@app.route('/login', methods=['POST'])
def login():
    print(request.path)
    data = request.form
    email = data.get('email')
    password = data.get('password')
    url = f'{users_url}/?email={email}&zipcode={password}'
    print(url)
    if not email or not password:
        return jsonify({'success': False, 'message': 'Missing email or password'}), 400

    response = requests.get(url)

    if response.status_code == 200:
        data_user = response.json()
        if data_user:
            return jsonify({'success': True, 'message': 'Login successful', 'user': data_user}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 404
    else:
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 400

@app.route('/register', methods=['POST'])
def signIn():
    print(request.path)
    data = request.form
    email = data.get('email')
    password = data.get('password')
    name = data.get('username')
    if not email or not password or not name:
        return jsonify({'success': False, 'message': 'Missing email or password'}), 400

    # register_server_jsonplaceholder(email, password, name)

    register_file_json(email, password, name)


def register_file_json(email, password, name):
    """ регистрация пользователя в BD json"""
    list_users = load_users() # Load list_users from the JSON file
    id = len(list_users) + 1
    print(len(list_users))
    if list_users:
        user = next((user for user in list_users if user['email'] == email), None)
        # user = find_user_by_email(email, list_users)
        print('finded user', user)
        if user:
            print("User already exists")
            return # jsonify({'success': False, 'message': 'Conflict: User already exists'}), 409

    user_data = {
        "id": id,
        "name": name,
        "email": email,
        "password": password
    }
    add_user_to_json(user_data, list_users)


def load_users():
    """ получает данные из файла json """
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            users = json.load(file)
            print(users)
        return users
    else:
        with open(filename, 'a') as file:
            file.write(json.dumps([]))
        return []


def find_user_by_email(email, users):
    for user in users:
        if user['email'] == email:
            return user
    return None


def add_user_to_json(user_data, list_users):
    """ добавить пользователя в файл json"""
    list_users.append(user_data)
    print(list_users)
    with open(filename, 'w') as file:
        file.write(json.dumps(list_users))


def register_server_jsonplaceholder(email, password, name):
    """ отправляет запрос регистрации на сервер jsonplaceholder"""
    url = f'{users_url}/?email={email}&zipcode={password}'
    if not email or not password:
        return jsonify({'success': False, 'message': 'Missing email or password'}), 400
    response = requests.get(url)
    if response.status_code == 200:
        exists_user = response.json()
        if exists_user:
            return jsonify({'success': False, 'message': 'User is exists'}), 400


def send_GET_Request(email, password):
    """ GET-запрос """
    url = f'{users_url}/?email={email}'
    response = requests.get(url, auth=(email, password), verify=True)
    # url = 'https://rickandmortyapi.com/api/character/?name=rick&status=alives'
    # response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        print('email, password: ', email, password)
        return data, response.status_code
    else:
        return [], response.status_code

# if __name__ == '__main__':
#     app.run(debug=True)

# send_GET_Reauest('Shanna@melissa.tv', '13142')
# send_GET_Reauest('ecovod203@esdl.us', 'asfdasd')
email = 'Shanna@melissa.tvs'
password = '111'
name = "Anna"
register_file_json(email, password, name)