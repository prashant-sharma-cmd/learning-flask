from flask import render_template, request, redirect, url_for
from models import Person, User
from flask_login import login_user, logout_user, current_user, login_required

def register_routes(app, db, bcrypt):

    @app.route('/', methods=['GET', 'POST'])
    def home():
        return render_template('home.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            hashed_password = bcrypt.generate_password_hash(password)

            user = User(username=username, password=hashed_password)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('home'))
        return ""

    @app.route('/login/', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username).first()

            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                return render_template('login.html')

        return ""


    @app.route('/logout/', methods=['GET', 'POST'])
    def logout():
        logout_user()
        return redirect(url_for('home'))

    @app.route('/index', methods=['GET', 'POST'])
    @login_required
    def index():
        if request.method == 'GET':
            people = Person.query.all()
            return render_template('index.html', people=people)
        elif request.method == 'POST':
            name = request.form['name']
            age = request.form['age']
            job = request.form['job']

            person = Person(name=name, age=age, job=job)

            db.session.add(person)
            db.session.commit()

            people = Person.query.all()
            return render_template('index.html', people=people)

        return ""

    @app.route('/delete/<pid>', methods=['DELETE'])
    def delete(pid):
        Person.query.filter(Person.pid == pid).delete()
        db.session.commit()
        people = Person.query.all()
        return render_template('index.html', people=people)

    @app.route('/details/<pid>')
    def details(pid):
        person = Person.query.filter(Person.pid == pid).first()
        return render_template('details.html', person=person)
