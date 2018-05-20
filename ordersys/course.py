from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from ordersys.auth import login_required
from ordersys.db import get_db

bp = Blueprint('course', __name__)

@bp.route('/')
def index():
    db = get_db()

    courses = db.execute(
        'SELECT c.id, c.title, c.description, c.image_url'
        ', c.price, c.quantity, c.status'
        ', created_by, created_at, updated_by, updated_at'
        ' FROM course as c'
        ' WHERE c.status == "on"'
        ' ORDER BY updated_at DESC'
    ).fetchall()

    return render_template('course/index.html', courses=courses)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        now = datetime.now()

        title = request.form['title']
        description = request.form['description']
        image_url = request.form['image_url']
        price = request.form['price']
        quantity = request.form['quantity']
        status = request.form['status']
        created_by = g.user['id']
        created_at = now
        updated_by = g.user['id']
        updated_at = now

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO course'
                ' (title, description, image_url, price, quantity, status'
                ', created_by, created_at, updated_by, updated_at)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (title, description, image_url, price, quantity, status,
                 created_by, created_at, updated_by, updated_at)
            )
            db.commit()
            return redirect(url_for('course.index'))

    return render_template('course/create.html')
