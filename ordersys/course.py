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
