

from werkzeug.security import generate_password_hash, check_password_hash

from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_names = db.Column(db.String(80), nullable=False)
    profile_pic = db.Column(db.String(80))

    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(124), nullable=False, server_default="")
    posts = db.relationship("PostModel", lazy="dynamic")

    @classmethod
    def find_user_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()


    @classmethod
    def encrypt_password(cls, plaintext_password):
        """
        Hash a plaintext string using PBKDF2. This is good enough according
        to the NIST (National Institute of Standards and Technology).

        In other words while bcrypt might be superior in practice, if you use
        PBKDF2 properly (which we are), then your passwords are safe.

        :param plaintext_password: Password in plain text
        :type plaintext_password: str
        :return: str
        """
        if plaintext_password:
            return generate_password_hash(plaintext_password)

        return None

    @classmethod
    def find_user_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()


    @classmethod
    def authenticated(cls,old_password:str, new_password: str):
        """
        Ensure a user is authenticated, and check their password.

        :param with_password: Optionally check their password
        :type with_password: bool
        :type password: str
        :return: bool
        """
        return check_password_hash(old_password, new_password)



    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
