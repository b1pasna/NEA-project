from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# database 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# sign up 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password for security
        hashed_password = generate_password_hash(password, method='sha256')

        # check if username or email already exists
        existing_user = User.query.filter((User.username==username)|(User.email==email)).first()
        if existing_user:
            flash("Username or email already exists!")
            return redirect(url_for('signup'))

        # add new user to the database
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please log in.")
        return redirect(url_for('login'))

    # GET request: render the signup form
    return render_template('signup.html')

# login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # fetch user from database
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # store user info in session
            session['user_id'] = user.id
            session['username'] = user.username
            flash("Logged in successfully!")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password!")
            return redirect(url_for('login'))

    # GET request: render the login form
    return render_template('login.html')

# logout 
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("Logged out successfully!")
    return redirect(url_for('home'))
