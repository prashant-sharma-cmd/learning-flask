from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return "<h1>You made a GET request! </h1>"
    elif request.method == 'POST':
        return "<h1>You made a POST request! </h1>"
    else:
        return "<h1>You won't ever access it! </h1>"

@app.route('/hi')
def hi():
    return "<h1>Hi World! </h1>", 200

@app.route('/fox')
def fox():
    response = make_response('Hello World!')
    response.status_code = 200
    response.headers['Content-Type'] = 'application/js'
    return response


@app.route('/hello/<name>')
def greet(name):
    return "<h1>Hello %s</h1>" % name

@app.route('/add/<int:number1>/<int:number2>')
def add(number1, number2):
    return f"{number1} + {number2} =  {number1 + number2}"

@app.route('/handle_url_params')
def handle_params():
    if 'name' in request.args.keys():
        name = request.args[
            "name"]  # If this is not provided it will return error
        greeting = request.args.get(
            "greeting")  # If not provided, returns None
        return f"{greeting} {name}"
    else:
        return "Some parameter is missing"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)