import os
import uuid
from flask import Flask, render_template, request, Response, send_from_directory, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            return "Success"

        return "Wrong username or password!!"
    else:
        return " "

@app.route('/file', methods=['POST'])
def file_upload():
    file = request.files['file']
    if file.content_type == 'text/plain':
        return file.read().decode()
    elif (file.content_type == ".xls" or file.content_type == ".xlsx" or
            file.content_type == "application/vnd.ms-excel" or
            file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or
            file.content_type == "application/vnd.ms-excel"):
        df = pd.read_excel(file)
        return df.to_html(index=True)
    return " "

@app.route('/convert_csv', methods=['POST'])
def convert_csv():
    file = request.files['file']
    if (file.content_type == ".xls" or file.content_type == ".xlsx" or
          file.content_type == "application/vnd.ms-excel" or
          file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or
          file.content_type == "application/vnd.ms-excel"):
        df = pd.read_excel(file)
        response = Response(
            df.to_csv(),
            mimetype="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=result.csv",
            }
        )
        return response
    return " "

@app.route('/convert_csv_two', methods=['POST'])
def convert_csv_two():
    file = request.files['file']
    if (file.content_type == ".xls" or file.content_type == ".xlsx" or
          file.content_type == "application/vnd.ms-excel" or
          file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or
          file.content_type == "application/vnd.ms-excel"):
        df = pd.read_excel(file)
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
        filename = f'{uuid.uuid4()}.csv'
        df.to_csv(os.path.join('downloads', filename))
        return render_template('download.html', filename=filename)
    return " "

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(directory='downloads', path=filename, download_name='result.csv')

@app.route('/handle_post', methods=['POST'])
def handle_post():
    greeting = request.json['greeting']
    name = request.json['name']

    with open('file.txt', 'w') as f:
        f.write(f'{greeting}, {name}')

    return jsonify({'message': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)