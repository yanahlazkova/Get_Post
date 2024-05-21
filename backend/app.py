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
    print("Login, method:", request.method)
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'success': False, 'message': 'Missing email or password'}), 400
        # data_user, status_code = send_GET_Reauest(email, password)
        url = f'{users_url}/?email={email}'
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            data_user = response.json()
            if len(data_user):
                # return jsonify({'success': True, 'message': 'Login successful', 'user': str(data_user)}), 200
                return jsonify({'success': True, 'message': 'Login successful', 'user': data_user}), 200
            else:
                return jsonify({'success': False, 'message': 'Invalid email or password'}), 400
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 400

def send_GET_Reauest(email, password):
    """ GET-запрос """
    url = f'{users_url}/?email={email}'
    response = requests.get(url, auth=(email, password), verify=True)
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