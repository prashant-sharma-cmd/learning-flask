from flask import Flask, render_template, session, make_response, request, flash

app = Flask(__name__, template_folder='templates')
app.secret_key = 'SOME KEY'


@app.route('/')
def index():
    return render_template('index.html', message='Index')

@app.route('/set_data')
def set_data():
    session['name'] = "Quin"
    session['sex'] = "Male"
    return render_template('index.html', message='Session Data Set')

@app.route('/get_data')
def get_data():
    if 'name' in session.keys() and 'sex' in session.keys():
        name = session['name']
        sex = session['sex']
        return render_template('index.html', message=f'Name: {name}, Sex: {sex}')
    else:
        return "Missing Session Data"

@app.route('/clear_session')
def clear_session():
    session.clear()
    # session.pop('name') For removing only one session data
    return render_template('index.html', message = "Session Data Cleared!!")

@app.route('/set_cookie')
def set_cookie():
    response = make_response(render_template('index.html', message='Cookie Set.'))
    response.set_cookie('name', 'brian')
    response.set_cookie('sex', 'trans')

    return response

@app.route('/get_cookie')
def get_cookie():
    name = request.cookies['name']
    sex = request.cookies['sex']
    return render_template('index.html', message=f"Name: {name} Sex:{sex}")

@app.route('/clear_cookie')
def clear_cookie():
    response = make_response(render_template('index.html', message='Cookie Deleted.'))
    response.set_cookie('name', expires=0)
    response.set_cookie('sex', expires=0)
    return response

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password':
            flash('Successful Login')
            return render_template('index.html', message='')
        else:
            flash('Login Failed')
            return render_template('login.html', message='')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)