import requests

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

users_url = 'https://jsonplaceholder.typicode.com/users'

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
    data_user = data.to_dict()
    print(data)
    # name = data.get('username')
    email = data.get('email')
    password = data.get('password')
    url = f'{users_url}/?email={email}&zipcode={password}'
    if not email or not password:
        return jsonify({'success': False, 'message': 'Missing email or password'}), 400
    response = requests.post(url, data_user)
    print(response.status_code)
    if response.status_code == 200:
        return jsonify({'success': False, 'message': 'User is exists'}), 400

    elif response.status_code == 404:
        response_post = requests.post(users_url, data_user)
        print(response_post.status_code)
        if response_post.status_code == 201:
            return jsonify({'success': True, 'message': 'User added', 'user': data}), 201
    else:
        return jsonify({'success': False, 'message': 'User did not add'}), response.status_code

def send_GET_Reauest(email, password):
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