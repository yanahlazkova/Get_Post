import requests
import json
import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

users_url = 'https://jsonplaceholder.typicode.com/users'


class Server:
    def __init__(self, filename):
        self.filename = filename
        self.app = Flask(__name__)
        CORS(self.app)
        self.setup_routes_login()
        self.setup_routes_signin()

    def setup_routes_login(self):
        self.app.route('/login', methods=['POST'])(self.login)

    def setup_routes_signin(self):
        self.app.route('/register', methods=['POST'])(self.signin)

    def login(self):
        print(request.path)
        data = request.form
        if not data:
            return jsonify({'success': False, 'message': 'Invalid data'}), 400
        required_fields = ['email', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        list_users = self.load_list_users_from_file()  # Load list_users from the JSON file
        if list_users:
            user = next((user for user in list_users if
                         (user['email'] == data.get('email') and user['password'] == data.get('password'))), None)
            print('found user', user)
            if user:
                print("User is exists", user)
                return jsonify({'success': True, 'message': 'Login successful', 'user': user}), 200

            else:
                return jsonify({'success': False, 'message': 'User not found'}), 404

    def load_list_users_from_file(self):
        """ получает данные из файла json """
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                users = json.load(file)
                print(users)
            return users
        else:
            with open(self.filename, 'a') as file:
                file.write(json.dumps([]))
            return []

    def run(self, debug=True):
        self.app.run(debug=debug)

    def signin(self):
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

        success, message, status_code = self.register_file_json(data)
        print("success", success, "status_code", status_code, "message", message)
        return jsonify({'success': success, 'message': message}), status_code

        # return  jsonify({'success': False, 'message': 'Conflict: User already exists'}), 409

    def register_file_json(self, data):
        """ регистрация пользователя в BD json"""
        list_users = self.load_list_users_from_file()  # Load list_users from the JSON file
        id = len(list_users) + 1

        print(len(list_users))
        print(data)
        if list_users:
            # user = next((user for user in list_users if user['email'] == email), None)
            # print('found user', user)
            if any(user['email'] == data['email'] for user in list_users):
                print("User already exists")
                return False, "User with this email already exists.", 409
        list_users.append(data)

        return self.add_user_to_file(list_users)

    def add_user_to_file(self, list_users):
        """ добавить пользователя в файл json"""
        print(list_users)
        try:
            with open(self.filename, 'w') as file:
                # file.write(json.dumps(list_users))
                json.dump(list_users, file, ensure_ascii=False, indent=4)
                return True, "User successfully added.", 201
        except (IOError, TypeError) as e:
            print(f'Error writing to file: {e}')
            return False, "Error writing to file.", 500

    def find_user_by_email(self, email, users):
        for user in users:
            if user['email'] == email:
                return user
        return None


if __name__ == '__main__':
    server = Server(users_url)
    server.run()
