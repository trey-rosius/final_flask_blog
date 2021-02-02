from typing import List

from db import db


class PostModel(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    posts = db.Column(db.Text, nullable=False)
    image_url =db.Column(db.String(255),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    users = db.relationship("UserModel")
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    @classmethod
    def find_by_id(cls, _id) -> "PostModel":
        return cls.query.filter_by(id=_id).first()



    @classmethod
    def find_all_posts(cls) -> List["PostModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

