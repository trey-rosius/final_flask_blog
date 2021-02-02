import os

from flask import Flask
from dotenv import load_dotenv
from flask_uploads import configure_uploads, patch_request_class

import config
from blueprints import contact, auth, blog, profile
from db import db
from libs.image_helper import IMAGE_SET
from ma import ma

app = Flask(__name__, instance_relative_config=True)
load_dotenv(".env", verbose=True)

app.config.from_mapping(
    SECRET_KEY='this once',
    SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    PROPAGATE_EXCEPTIONS=True,
    UPLOADED_IMAGES_DEST=os.path.join("static", "images"),

)

patch_request_class(app, 10 * 1024 * 1024)
configure_uploads(app, IMAGE_SET)

db.init_app(app)
ma.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)
app.add_url_rule('/', endpoint='index')
app.register_blueprint(contact.bp)
app.register_blueprint(profile.bp)

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000, debug=True)
