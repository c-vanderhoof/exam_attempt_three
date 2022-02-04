from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models import magazine, user

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    mags=magazine.Magazine.get_all()
    user_data = {
        "id": session['user_id']
    }
    return render_template('dashboard.html', mags=mags, this_user=user.User.get_by_id(user_data))


@app.route('/new')
def new_mag():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('new_magazine.html')

@app.route('/create_mag',methods=['POST'])
def create_mag():
    if 'user_id' not in session:
        return redirect('/logout')
    if not magazine.Magazine.validate_mag(request.form):
        return redirect('/new')
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "user_id": session['user_id']
    }
    magazine.Magazine.save(data)
    return redirect('/dashboard')

@app.route('/delete/magazine/<int:id>')
def delete_mag(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    magazine.Magazine.delete_magazine(data)
    return redirect('/user/account')

@app.route('/user/account')
def show_user():
    if 'user_id' not in session:
        return redirect('/logout')
    mag_data = {
        "user_id": session['user_id']
    }
    magazines= magazine.Magazine.get_by_user_id(mag_data)
    return render_template('user.html', magazines=magazines)

@app.route('/show/<int:id>')
def show_mag(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id":id
    }
    mag=magazine.Magazine.get_by_id(data)
    user_data= {
        "id": mag.user_id
        }
    usr= user.User.get_by_id(user_data)
    return render_template('show_magazine.html',this_mag=mag, some_user=usr)