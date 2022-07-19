import json
from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, redirect, send_file, url_for, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app import db, generate_random_code, app
from app.models import User, File
import os
import datetime
from flask_tor import run_with_tor


from werkzeug.security import generate_password_hash

upload_directory = "uploads/"
domain = "http://127.0.0.1:5000/"
# port = run_with_tor()

@app.route('/login')
def login():
    return render_template('login.html', user = current_user)

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    # # Use this to add new users if needed
    # u = User(email = "XYZ@gmail.com", password = generate_password_hash("12345"), name = "Saad")
    # db.session.add(u)
    # db.session.commit()

    # # to delete all files - caution
    # f = File.query.delete()
    # db.session.commit()

    last = None
    if current_user.is_authenticated:
        last = File.query.first()
        if last:
            last = last.id
    return render_template('index.html', user = current_user, last = last)
    
@app.route('/upload', methods = ["POST"])
@login_required
def upload():
    file = request.files["file"]
    print(file, flush = True)
    if file.filename == '':
        flash('No selected file')
    if file:
        extension = os.path.splitext(file.filename)[1]
        if extension == ".hc":
            f = File(name = file.filename)
            db.session.add(f)
            db.session.commit()
            file.save(os.path.join(upload_directory, str(f.id) + ".hc"))
    return redirect(url_for("index"))

@app.route('/download/<code>', methods = ["GET"])
@login_required
def download(code):
    fo = File.query.filter_by(id = code).first()
    if fo:
        path = os.path.abspath(upload_directory + "/" + code + ".hc")
        return send_file(path, as_attachment = True, attachment_filename = fo.name)
    else:
        return render_template("notfound.html", user = current_user)

@app.route('/delete/<code>', methods = ["GET"])
@login_required
def delete(code):
    fo = File.query.filter_by(id = code)
    if fo:
        fo.delete()
        db.session.commit()
        return redirect(url_for("archive"))
    else:
        return jsonify(success = False)

@app.route('/archive', methods = ["GET"])
@login_required
def archive():
    page = request.args.get('page', 1, type=int)
    current = File.query.first()
    if current:
        current = current.id
    else:
        current = None
    files = db.session.query(File).filter(File.id != current).paginate(page=page, per_page = 10)

    last = File.query.first()
    if last:
        last = last.id

    return render_template('archive.html', files=files, user = current_user, last = last)

@app.route('/delete_all', methods = ["GET"])
@login_required
def delete_all():
    # to delete all files - caution
    current = File.query.first()
    if current:
        current = current.id
    else:
        current = None
    f = db.session.query(File).filter(File.id != current).delete()
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    # app.run(port = port)
    app.run(debug = True)