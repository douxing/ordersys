from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from ordersys.auth import login_required
from ordersys.db import get_db

bp = Blueprint('course', __name__)

@bp.route('/')
def index():
    db = get_db()

    courses = db.execute(
        'SELECT c.id, c.title, c.description, c.icon_hashname'
        ', c.price, c.status'
        ', created_by, created_at, updated_by, updated_at'
        ' FROM course as c'
        # ' WHERE c.status == "on"'
        ' ORDER BY updated_at DESC'
    ).fetchall()

    return render_template('course/index.html', courses=courses)

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
            return redirect(url_for('course.index'))

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
        return redirect(url_for('course.index'))    
