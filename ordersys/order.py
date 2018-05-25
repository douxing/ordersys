from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from ordersys.auth import login_required
from ordersys.db import get_db

bp = Blueprint('order', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('order/index.html')

@bp.route('/<int:id>/view')
@login_required
def view(id):
    is_admin = g.user['is_admin']

    db = get_db()

    course = db.execute(
        'SELECT o.price, o.status,'
        ' o.table_no, o.take_out_address, o.take_out_phone_no,'
        ' o.created_by, o.created_at, o.updated_by, o.updated_at'
        " FROM 'order' as o"
        ' WHERE o.id = ?'
        (id, )
    ).fetchone()

    if course is None:
        abort(404, "Course id {0} doesn't exist.".format(id))
        
    if course['updated_by'] != g.user['id']:
        abort(403)

    return render_template('course/index.html', courses=courses)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    ids = {}
    for idx in request.form:
        try:
            index = int(idx)
            quantity = int(request.form[idx])

            if quantity > 0:
                ids[index] = quantity
        except:
            continue

    if len(ids) == 0:
        flash('请添加菜品:)')
        return redirect(url_for('course.index'))

    db = get_db()
    cursor = db.cursor()

    courses = cursor.execute(
        'SELECT c.id, c.title, c.description, c.icon_hashname'
        ', c.price, c.quantity, c.status'
        ', created_by, created_at, updated_by, updated_at'
        ' FROM course as c'
        ' WHERE c.id IN ({})'.format(','.join('?' * len(ids))),
        [idx for idx in ids]
    ).fetchall()

    if len(courses) != len(ids):
        flash('发生错误,请重新选择:(')
        return redirect(url_for('course.index'))

    price = 0
    for course in courses:
        price += ids[course['id']] * course['price']

    now = datetime.now()
    cursor.execute(
        "INSERT INTO 'order' (status, price, table_no,"
        ' take_out_address, take_out_phone_no'
        ', created_by, created_at, updated_by, updated_at)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        ('new', price, 0, '', '', g.user['id'], now, g.user['id'], now)
    )

    order_id = cursor.lastrowid;
    order_courses = []

    for course in courses:
        course_id = course['id']

        order_courses.append((
            order_id, course_id,
            course['title'], course['description'],
            course['icon_hashname'], course['price'],
            ids[course_id]
        ))

    cursor.executemany(
        'INSERT INTO order_course (order_id , course_id,'
        ' title, description, icon_hashname, '
        ' price, quantity) VALUES (?, ?, ?, ?, ?, ?, ?)',
        order_courses
    )

    db.commit()

    return redirect(url_for('order.update', id=order_id))

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    is_admin = g.user['is_admin']

    db = get_db()

    if request.method == 'POST':
        pass
    else: # GET

        order = db.execute(
            'SELECT o.id, o.price, o.status,'
            ' o.table_no, o.take_out_address, o.take_out_phone_no,'
            ' o.created_by, o.created_at, o.updated_by, o.updated_at'
            " FROM 'order' as o"
            ' WHERE o.id = ?',
            (id, )
        ).fetchone()

        if order is None:
            abort(404, "Order id {0} doesn't exist.".format(id))
        
        if order['created_by'] != g.user['id'] or not is_admin:
            abort(403)

        courses = db.execute(
            'SELECT * FROM order_course WHERE order_id = ?',
            (id, )
        ).fetchall()

        return render_template('order/update.html', order=order, courses=courses)
