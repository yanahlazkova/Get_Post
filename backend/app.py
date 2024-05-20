from flask import Flask, render_template, request, jsonify
import 

app = Flask(__name__)

@app.route('/')
def home():
    # return "Hello from Flask!"
    return render_template('home.html')

@app.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        email = request.form['logemail']
        password = request.form['logpass']
        print('email: pass', email, password)
        return jsonify({'success': True, 'message': 'Login successful'}), 200
            
    else:
        return jsonify({'success': False, 'message': 'Invalid email or password'})



if __name__ == '__main__':
    app.run(debug=True)
