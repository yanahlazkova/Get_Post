import requests
import json
import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

users_url = 'https://jsonplaceholder.typicode.com/users'
# filename = 'database.json'
filename = 'users.json'

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
    if not data:
        return jsonify({'success': False, 'message': 'Invalid data'}), 400
    required_fields = ['email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    list_users = load_list_users_from_file() # Load list_users from the JSON file
    if list_users:
        user = next((user for user in list_users if user['email'] == data.get('email')), None)
        # print('found user', user)
        if user:
            print("User is exists", user)
            return jsonify({'success': True, 'message': 'Login successful', 'user': user}), 200

        else:
            return jsonify({'success': False, 'message': 'User did not exists'}), 404

@app.route('/register', methods=['POST'])
def signIn():
    print(request.path)
    data = request.form
    print(data)
    # if not email or not password or not name:
    if not data:
        return jsonify({'success': False, 'message': 'Invalid data'}), 400
    required_fields = ['name', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    # register_server_jsonplaceholder(email, password, name)

    success, message, status_code = register_file_json(data)
    return jsonify({'success': success, 'message': message}), status_code

    # return  jsonify({'success': False, 'message': 'Conflict: User already exists'}), 409


def register_file_json(data):
    """ регистрация пользователя в BD json"""
    list_users = load_list_users_from_file() # Load list_users from the JSON file
    id = len(list_users) + 1
    print(len(list_users))
    if list_users:
        # user = next((user for user in list_users if user['email'] == email), None)
        # print('found user', user)
        if any(user['email'] == data['email'] for user in list_users):
            print("User already exists")
            return False, "User with this email already exists.", 409
    list_users.append(data)

    return add_user_to_file(list_users)


def load_list_users_from_file():
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


def add_user_to_file(list_users):
    """ добавить пользователя в файл json"""
    print(list_users)
    try:
        with open(filename, 'w') as file:
            # file.write(json.dumps(list_users))
            json.dump(list_users, file, ensure_ascii=False, indent=4)
            return True, "User successfully added.", 201
    except (IOError, TypeError) as e:
        print(f'Error writing to file: {e}')
        return False, "Error writing to file.", 500


def find_user_by_email(email, users):
    for user in users:
        if user['email'] == email:
            return user
    return None


def login_server_jsonplaceholder(data):
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

if __name__ == '__main__':
    app.run(debug=True)

# send_GET_Reauest('Shanna@melissa.tv', '13142')
# send_GET_Reauest('ecovod203@esdl.us', 'asfdasd')
# data = {
#     'email' : 'Shanna@melissa.tv',
#     'password' : '111',
#     'name' : "Anna"
# }
# register_file_json(data)
