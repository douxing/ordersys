from datetime import datetime
import hashlib
import base64
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from ordersys.auth import login_required
from ordersys.db import get_db

bp = Blueprint('course', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()

    courses = db.execute(
        'SELECT c.id, c.title, c.description, c.icon_hashname'
        ', c.price, c.status'
        ', created_by, created_at, updated_by, updated_at'
        ' FROM course as c'
        ' WHERE c.status == "online"'
        ' ORDER BY updated_at DESC'
    ).fetchall()

    return render_template('course/index.html', courses=courses)

@bp.route('/all')
@login_required
def all():
    if not g.user['is_admin']:
        abort(401)

    db = get_db()

    courses = db.execute(
        'SELECT c.id, c.title, c.description, c.icon_hashname'
        ', c.price, c.status'
        ', created_by, created_at, updated_by, updated_at'
        ' FROM course as c'
        ' ORDER BY updated_at DESC'
    ).fetchall()

    return render_template('course/all.html', courses=courses)

@bp.route('/menuicons')
@login_required
def menuicons():
    db = get_db()
    
    icons = db.execute(
        'SELECT mi.hashname FROM menuicon as mi'
    ).fetchall()

    
    icons = [icon['hashname'] for icon in icons]

    return jsonify(icons)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    is_admin = g.user['is_admin']

    if not is_admin:
        abort(401)

    try:
        icon_hashname = request.form['icon_hashname']
    except KeyError:
        icon_hashname = 'default.png'

    if request.method == 'POST':
        now = datetime.now()

        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        status = request.form['status']
        created_by = g.user['id']
        created_at = now
        updated_by = g.user['id']
        updated_at = now

        error = None

        if not title:
            error = 'Title is required.'
        elif not description:
            error = 'Description is required'
        else:
            try:
                price = round(float(price), 2)
            except:
                error = 'Price format error'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO course'
                ' (title, description, icon_hashname, price, status'
                ', created_by, created_at, updated_by, updated_at)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (title, description, icon_hashname, price, status,
                 created_by, created_at, updated_by, updated_at)
            )
            db.commit()
            return redirect(url_for('course.all'))

    return render_template('course/create.html', icon_hashname=icon_hashname)

@bp.route('/<int:id>/view')
@login_required
def view(id):
    pass
    
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    is_admin = g.user['is_admin']

    if not is_admin:
        abort(401)

    db = get_db()

    course = db.execute(
        'SELECT * FROM course WHERE id=?',
        (id, )
    ).fetchone()

    if request.method == 'GET':
        return render_template('course/update.html', course=course)

    try:
        icon_hashname = request.form['icon_hashname']
    except KeyError:
        icon_hashname = 'default.png'

    now = datetime.now()
    
    title = request.form['title']
    description = request.form['description']
    price = request.form['price']
    status = request.form['status']
    created_by = g.user['id']
    created_at = now
    updated_by = g.user['id']
    updated_at = now

    error = None

    if not title:
        error = 'Title is required.'
    elif not description:
        error = 'Description is required'
    else:
        try:
            price = round(float(price), 2)
        except:
            error = '价格格式错误:('

    if error is not None:
        flash(error)
        return render_template('course/update.html', course=course)
    else:
        db.execute(
            'UPDATE course SET'
            ' title=?, description=?, icon_hashname=?, price=?, status=?'
            ', created_by=?, created_at=?, updated_by=?, updated_at=?'
            ' WHERE id=?',
            (title, description, icon_hashname, price, status,
             created_by, created_at, updated_by, updated_at, id)
        )
        db.commit()
        return redirect(url_for('course.all'))    

def get_extension(filename):
    if '.' in filename:
        ext = filename.rsplit('.', 1)[1]
        if ext in ['jpeg', 'jpg', 'gif', 'ico', 'png', 'img']:
            return ext

    return None

@bp.route('/upload_icon', methods=['POST'])
@login_required
def upload_icon():
    if not g.user['is_admin']:
        abort(401)

    if request.files['file']:
        iconfile = request.files['file']
        ext = get_extension(iconfile.filename)
        content = iconfile.read()

        if len(content) > 10000000:
            abort(403) # too big

        sha256 = hashlib.sha256()
        sha256.update(content)
        sha256 = sha256.digest()
        name = str(base64.urlsafe_b64encode(sha256), 'utf-8') + '.' + ext

        print('content.length: {}'.format(len(content)))

        try:
            folder = os.path.dirname(os.path.abspath(__file__))
            f = open(os.path.join(folder, 'static/menuicons', name), 'wb')
            f.write(content)
            f.close()
        except Exception as e:
            print('error on save: {}'.format(e))
            abort(403)

        try:
            db = get_db()
            db.execute(
                'INSERT OR REPLACE INTO menuicon'
                ' (hashname)'
                ' VALUES(?)',
                (name, )
            )
            db.commit()
        except Exception as e:
            print('error on save: {}'.format(e))
            abort(403)            
        
        return jsonify({
            'name': name
        })

    return abort(403)
