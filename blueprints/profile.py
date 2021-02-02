import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_uploads import UploadNotAllowed
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from libs import image_helper
from models.post import PostModel
from models.user import UserModel


bp = Blueprint('profile', __name__)

@bp.route('/user/<int:id>/profile',methods=('GET',))
def get(id):
    user = UserModel.find_user_by_id(id)
    if not user:
        flash("User doesn't exist")

    return render_template('profile/profile.html', user= user)

@bp.route('/user/<int:id>', methods=('GET', 'POST'))
def update(id):
    user = UserModel.find_user_by_id(id)
    if not user:
        flash("User doesn't exist")
    if request.method == 'POST':
        full_names = request.form['full_names']
        image_file = request.files['file']

        error = None

        if not full_names:
            error = "Full Names Required"

        if error is not None:
            flash(error)
        if not image_file:
            flash("Please Attach a file")
        else:

            filename = f"user_{g.user.id}"
            folder = "avatars"
            try:
                ext = image_helper.get_extension(image_file.filename)
                avatar = filename + ext
                image_path = image_helper.save_image(image_file,
                                                     folder=folder,name=avatar)
                basename = image_helper.get_path(image_path)
                user.full_names = full_names
                user.profile_pic = image_path
                user.save_to_db()

                #post = PostModel(title=title, posts=body, image_url=image_path, user_id=userModel.id)
                #post.save_to_db()

            except UploadNotAllowed:
                extension = image_helper.get_extension(image_file)
                flash("file with extension {} not allowed".format(extension))

            return redirect(url_for('profile.get',id=user.id))
    return render_template('/profile/edit_profile.html', user=user)





