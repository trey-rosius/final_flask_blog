import json
import os

import boto3
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,jsonify
)
from flask_uploads import UploadNotAllowed


from blueprints.auth import login_required, get_post
from libs import image_helper
from models.post import PostModel
from models.user import UserModel
from schema.post import PostSchema

bp = Blueprint('blog', __name__)

post_schema = PostSchema()
@bp.route('/post/json')
def allPosts():
    return {"posts": post_schema.dump(PostModel.find_all_posts(), many=True)}, 200

@bp.route('/')
def index():
    posts = PostModel.find_all_posts()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    bucket = 'rosius'
    content_type = request.mimetype
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        image_file = request.files['file']
        client = boto3.client('s3',
                              region_name='us-east-2',
                              endpoint_url='https://s3.us-east-2.amazonaws.com',
                              aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
                              aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        if not image_file:
            flash("Please Attach a file")
        else:

            folder = f"user_{g.user.id}"  # static/images
            try:
                if image_helper.is_filename_safe(image_file):
                    client.put_object(Body=image_file,
                                      Bucket=bucket,
                                      Key=image_file.filename,
                                      ACL="public-read",
                                      ContentType=content_type)
                    #image_path = image_helper.save_image(image_file,folder=folder)
                    #basename = image_helper.get_path(image_path)
                    print("https://rosius.s3.us-east-2.amazonaws.com/"+image_file.filename)
                    userModel = UserModel.find_user_by_id(g.user.id)
                    post = PostModel(title=title, posts=body, image_url="https://rosius.s3.us-east-2.amazonaws.com/"+image_file.filename, user_id=userModel.id)
                    post.save_to_db()



            except UploadNotAllowed:
                extension = image_helper.get_extension(image_file)
                flash("file with extension {} not allowed".format(extension))

            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.posts = body
            post.save_to_db()

            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    post.delete()
    return redirect(url_for('blog.index'))
