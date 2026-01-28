from flask import Flask, render_template, redirect, url_for

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    my_value = 20
    my_result = my_value * 2
    return render_template('index.html', value=my_value, result=my_result)

@app.route('/about')
def about():
    some_text = "Hello World"
    return render_template('about.html', text=some_text)

@app.route('/redirect_endpoint')
def redirect_endpoint():
    return redirect(url_for('about'))

@app.template_filter('reverse_string')
def reverse_string(text):
    return text[::-1]

@app.template_filter('repeat_string')
def repeat_string(text, count=2):
    return (text+" ")*count

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)