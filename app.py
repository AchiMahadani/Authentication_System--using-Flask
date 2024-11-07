from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "Welcome"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        print("Form submitted with email:", email)  # Debug statement

        user = User.query.filter_by(email=email).first()
        
        if user:
            print("User found:", user.email)  # Debug statement
        else:
            print("User not found")  # Debug statement

        if user and user.check_password(password):
            print("Password is correct")  # Debug statement
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            print("Invalid credentials")  # Debug statement
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html', user=user)
    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
