from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models import magazine
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id =User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/user/account')
def update_user():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id": session['user_id']
    }
    mag_data = {
        "user_id": session['user_id']
    }
    return render_template('user.html',user=User.get_by_id(user_data),magazines=magazine.Magazine.get_by_user_id(mag_data))

@app.route('/update/user', methods=['POST'])
def update_u():
    if 'user_id' not in session:
        return redirect('/logout')
    if not User.validate_registration(request.form):
        return redirect('/user/account')
    user_data = {
        "id": session['user_id']
    }
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    User.update(data)
    return redirect('/user/account')

@app.route('/login',methods=['POST'])
def login():
    current_user = User.get_by_email(request.form)
    if not current_user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(current_user.password,request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = current_user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')