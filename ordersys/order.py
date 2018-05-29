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
    is_admin = g.user['is_admin']

    db = get_db()

    orders = db.execute(
        "SELECT * FROM 'order' where created_by=? order by created_at DESC",
        (g.user['id'], )
    ).fetchall()
    
    return render_template('order/index.html', orders=orders)

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
        'SELECT c.id, c.title, c.description'
        ', c.icon_hashname, c.price, c.status'
        ', created_by, created_at, updated_by, updated_at'
        ' FROM course as c'
        ' WHERE c.id IN ({})'.format(','.join('?' * len(ids))),
        [idx for idx in ids]
    ).fetchall()

    if len(courses) != len(ids):
        flash('发生错误,请重新选择:(')
        return redirect(url_for('course.index'))

    price = 0.0
    for course in courses:
        quantity = ids[course['id']]
        price += quantity * course['price']

    now = datetime.now()
    cursor.execute(
        "INSERT INTO 'order' (status, price, table_no"
        ', take_out_address, take_out_phone_no'
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

    return redirect(url_for('order.eito', id=order_id))


@bp.route('/<int:id>/eito', methods=['GET', 'POST'])
@login_required
def eito(id):
    is_admin = g.user['is_admin']

    db = get_db()

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

    if order['status'] != 'new':
        flash('无法更改已提交的订单！')
        return redirect(url_for('order.index', id=id))

    courses = db.execute(
        'SELECT * FROM order_course WHERE order_id = ?',
        (id, )
    ).fetchall()

    if request.method == 'POST':
        cursor = db.cursor()
        error = None

        eito = request.form['eatintakeout']

        print("eatin or takeout: {}".format(eito))
        
        if eito == 'eatin':
            try:
                table_no = request.form['table_no']
                print("table number: {}".format(table_no))

                table_no = int(table_no)

                print("table number: {}, order id: {}".format(table_no, id))

                if table_no <= 0 or table_no > g.table_counter:
                    error = '桌号错误，请重试:('
                else:
                    cursor.execute(
                        "UPDATE 'order' SET status=?, table_no=?"
                        ' WHERE id=?',
                        ('confirmed', table_no, id)
                    )
            except:
                error = '数据错误，请重试:('
        elif eito == 'takeout':
            address = request.form['takeout_address']
            phone = request.form['takeout_phone']

            if len(address) == 0 or len(phone) < 7:
                error = '数据错误，请重试:('
            else:
                cursor.execute(
                    "UPDATE 'order' SET status='confirmed'"
                    ", take_out_address=?, take_out_phone_no=?"
                    'WHERE id=?',
                    (address, phone, order['id'])
                )
        else:
            error = '数据错误，请重试:('

        if error:
            flash(error)
            print("error: {}".format(error))
            
            return render_template('order/eito.html', order=order, courses=courses)
        else:
            db.commit()
            return redirect(url_for('order.view', id=id))

    else: # GET
        return render_template('order/eito.html', order=order, courses=courses)

@bp.route('/<int:id>/view', methods=['GET'])
@login_required
def view(id):
    is_admin = g.user['is_admin']

    db = get_db()

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

    return render_template('order/view.html', order=order, courses=courses)
