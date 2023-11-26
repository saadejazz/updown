from werkzeug.security import check_password_hash
from flask import render_template, redirect, send_file, url_for, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app import db, app
from app.models import User, File
import os

upload_directory = '/uploads'

@app.route('/login')
def login():
    return render_template('login.html', user = current_user)

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email = email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        
        # if the user doesn't exist or password is wrong, reload the page
        return redirect(url_for('login')) 

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember = remember)
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    # # to delete all files - caution
    # f = File.query.delete()
    # db.session.commit()

    last = None
    if current_user.is_authenticated:
        last = File.query.order_by(File.timestamp.desc()).first()
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
        # extension = os.path.splitext(file.filename)[1]
        # if extension == ".hc":
        f = File(name = file.filename)
        db.session.add(f)
        db.session.commit()
        file.save(os.path.join(upload_directory, str(f.id)))
    return redirect(url_for("index"))

@app.route('/download/<code>', methods = ["GET"])
@login_required
def download(code):
    f = File.query.filter_by(id = code).first()
    if f:
        path = os.path.abspath(upload_directory + "/" + code)
        return send_file(path, as_attachment = True, download_name = f.name)
    else:
        return render_template("notfound.html", user = current_user)

@app.route('/delete/<code>', methods = ["GET"])
@login_required
def delete(code):
    f = File.query.filter_by(id = code)
    file_path = os.path.abspath(upload_directory + "/" + code)
    if os.path.exists(file_path) and f:
        os.remove(file_path)
        f.delete()
        db.session.commit()
        return redirect(url_for("archive"))
    else:
        return jsonify(success = False)

@app.route('/archive', methods = ["GET"])
@login_required
def archive():
    page = request.args.get('page', 1, type = int)
    current = File.query.order_by(File.timestamp.desc()).first()
    if current:
        current = current.id
    else:
        current = None
    files = db.session.query(File).filter(File.id != current).paginate(page = page, per_page = 10)

    last = File.query.order_by(File.timestamp.desc()).first()
    if last:
        last = last.id

    return render_template('archive.html', files = files, user = current_user, last = last)

@app.route('/delete_all', methods = ["GET"])
@login_required
def delete_all():
    # to delete all files - caution
    current = File.query.order_by(File.timestamp.desc()).first()
    if current:
        current = current.id
    else:
        current = None
    query = db.session.query(File).filter(File.id != current)
    for f in query:
        file_path = os.path.abspath(upload_directory + "/" + str(f.id))
        if os.path.exists(file_path) and f:
            os.remove(file_path)
    query.delete()
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    # app.run(port = port)
    app.run(debug = True)