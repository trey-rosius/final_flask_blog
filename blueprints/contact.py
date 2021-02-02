from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)


bp = Blueprint('contact', __name__)
@bp.route('/contact')
def send_email():

    return render_template('contact/contact.html')
